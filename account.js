import { guestKey, readProgress, saveProgress, rateProgress, mergeProgress } from "./progress.js?v=2";
import {
  activityKey, deviceId, readActivity, saveActivity, recordReview, addActivity, combineActivity,
  toRows, fromRow, readOthers, saveOthers,
} from "./activity.js?v=1";

const apiUrl = "https://mosmevfnxnnxxmmktfcb.supabase.co";
const publishableKey = "sb_publishable_B2CkIOCAUSm_uEg7nN7rAQ_MPAI7XU4";
const minPasswordLength = 8;
const oauthKey = "maths-flashcards.oauth";
const providersKey = "maths-flashcards.providers";
const pointerFine = window.matchMedia("(hover: hover) and (pointer: fine)");

const views = {
  signin: {
    title: "Welcome back",
    intro: "Sign in to sync your progress across your devices.",
    submit: "Sign in", email: true, password: true, tabs: true,
  },
  signup: {
    title: "Create an account",
    intro: "Save your progress and pick up where you left off on any device.",
    submit: "Create account", email: true, password: true, tabs: true,
  },
  forgot: {
    title: "Reset your password",
    intro: "Enter your email and we’ll send you a link to choose a new password.",
    submit: "Send reset link", email: true,
  },
  recovery: {
    title: "Choose a new password",
    intro: "Use at least 8 characters.",
    submit: "Save password", password: true,
  },
  sent: { title: "Check your email", intro: "" },
  account: { title: "Your account", intro: "" },
};

// Supabase sends people back with tokens or an error in the URL fragment.
function readCallback() {
  const params = new URLSearchParams(location.hash.slice(1));
  let oauth = null;
  try {
    oauth = sessionStorage.getItem(oauthKey);
    sessionStorage.removeItem(oauthKey);
  } catch {}
  if (params.has("error") || params.has("error_code")) {
    history.replaceState(history.state, "", location.pathname + location.search);
    let error = "That link didn’t work. Please try again.";
    if (params.get("error_code") === "otp_expired") error = "That link has expired or has already been used. Request a new one.";
    else if (oauth) error = "Google sign-in didn’t finish. Please try again.";
    return { error };
  }
  if (params.has("setup")) history.replaceState(history.state, "", location.pathname + location.search);
  if (!params.has("access_token")) return { type: null };
  return { type: params.get("type") ?? (oauth ? "oauth" : null) };
}

// Shows “Continue with Google” only once Google is switched on for the project.
async function googleEnabled() {
  try {
    const cached = sessionStorage.getItem(providersKey);
    if (cached) return cached === "google";
  } catch {}
  try {
    const response = await fetch(apiUrl + "/auth/v1/settings", {
      headers: { apikey: publishableKey },
      signal: AbortSignal.timeout(8_000),
    });
    const settings = await response.json();
    const enabled = settings?.external?.google === true;
    try { sessionStorage.setItem(providersKey, enabled ? "google" : "email"); } catch {}
    return enabled;
  } catch {
    return false;
  }
}

// Creates a confirmed account through the project's create-account Edge Function,
// so sign-up doesn't wait on Supabase's rate-limited confirmation emails.
async function createAccount(email, password) {
  let response;
  try {
    response = await fetch(apiUrl + "/functions/v1/create-account", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
      signal: AbortSignal.timeout(15_000),
    });
  } catch {
    throw { name: "AuthRetryableFetchError" };
  }
  if (response.ok) return;
  const body = await response.json().catch(() => ({}));
  throw { code: body.code, status: response.status };
}

function errorMessage(error) {
  switch (error?.code) {
    case "invalid_credentials": return "That email and password don’t match.";
    case "email_not_confirmed": return "Confirm your email first. Check your inbox for the link we sent.";
    case "user_already_exists":
    case "email_exists": return "There’s already an account with that email. Sign in instead.";
    case "weak_password": return "Choose a stronger password with at least 8 characters.";
    case "same_password": return "Choose a password you haven’t used before.";
    case "signup_disabled":
    case "email_provider_disabled": return "New accounts can’t be created right now.";
    case "email_address_invalid": return "Enter a valid email address.";
    case "email_address_not_authorized": return "The site can’t send emails to that address yet.";
    case "over_email_send_rate_limit": return "Too many emails sent. Wait a while and try again.";
    case "over_request_rate_limit": return "Too many attempts. Wait a minute and try again.";
  }
  if (error?.status === 429) return "Too many attempts. Wait a minute and try again.";
  if (!navigator.onLine || error?.name === "AuthRetryableFetchError") return "Couldn’t connect. Check your connection and try again.";
  return "Something went wrong. Please try again.";
}

export function connectAccount(ui, onProgress, toast = () => {}, onActivity = () => {}) {
  const dialog = ui["account-dialog"];
  const form = ui["sign-in-form"];
  const emailInput = ui["account-email"];
  const passwordInput = ui["account-password"];
  const message = ui["account-message"];
  const submit = ui["sign-in-submit"];
  const callback = readCallback();
  const redirectTo = location.origin + location.pathname;
  const client = window.supabase?.createClient(apiUrl, publishableKey, {
    auth: { flowType: "implicit", detectSessionInUrl: true, storageKey: "maths-flashcards.session.v1" },
  });
  const device = deviceId();
  let progress = readProgress();
  let activity = readActivity();
  let others = new Map();
  let google = false;
  let profile = null;
  let view = "signin";
  let sentText = "";
  let syncState = "";
  let syncTimer;

  function currentView() {
    return profile && view !== "recovery" ? "account" : view;
  }

  function renderAccountButton() {
    const button = ui["account-button"];
    const initial = profile?.email?.[0]?.toUpperCase() ?? "";
    button.classList.toggle("signed-in", Boolean(profile));
    button.dataset.sync = profile ? syncState : "";
    ui["account-avatar"].hidden = !profile;
    ui["account-avatar"].textContent = initial;
    ui["account-avatar-large"].textContent = initial;
    ui["account-label"].textContent = profile ? "Account" : "Sign in";
    button.setAttribute("aria-label", profile ? "Account, signed in as " + profile.email : "Sign in");
  }

  function renderAccount() {
    const current = currentView();
    const config = views[current];
    ui["account-title"].textContent = config.title;
    ui["account-intro"].textContent = config.intro;
    form.hidden = !config.submit;
    ui["auth-tabs"].hidden = !config.tabs;
    ui["google-option"].hidden = !(google && config.tabs);
    ui["auth-tabs"].dataset.active = current;
    ui["tab-signin"].setAttribute("aria-pressed", String(current === "signin"));
    ui["tab-signup"].setAttribute("aria-pressed", String(current === "signup"));
    ui["email-field"].hidden = !config.email;
    emailInput.disabled = !config.email;
    ui["password-field"].hidden = !config.password;
    passwordInput.disabled = !config.password;
    passwordInput.autocomplete = current === "signin" ? "current-password" : "new-password";
    passwordInput.minLength = current === "signin" ? 1 : minPasswordLength;
    ui["password-hint"].hidden = current === "signin";
    ui["forgot-password"].hidden = current !== "signin";
    ui["submit-label"].textContent = config.submit ?? "";
    ui["back-to-sign-in"].hidden = current !== "forgot";
    ui["check-email"].hidden = current !== "sent";
    ui["check-email-text"].textContent = sentText;
    ui["signed-in-panel"].hidden = current !== "account";
    ui["guest-note"].hidden = Boolean(profile) || current === "recovery";
    ui["account-email-label"].textContent = profile?.email ?? "";
    renderAccountButton();
  }

  function focusFirstField() {
    const current = currentView();
    if (current === "account") return ui["sign-out"].focus();
    if (current === "sent") return ui["check-email-back"].focus();
    if (!pointerFine.matches) return ui["account-close"].focus();
    const skipEmail = emailInput.disabled || (current === "signin" && emailInput.value);
    (skipEmail ? passwordInput : emailInput).focus();
  }

  function setView(next, { keepMessage = false } = {}) {
    view = next;
    if (!keepMessage) message.textContent = "";
    renderAccount();
    if (dialog.open) {
      const panel = !form.hidden ? form : !ui["check-email"].hidden ? ui["check-email"] : ui["signed-in-panel"];
      panel.classList.remove("view-enter");
      void panel.offsetWidth;
      panel.classList.add("view-enter");
      focusFirstField();
    }
  }

  function openAccount(next) {
    if (next) view = next;
    else if (!profile && view === "sent") view = "signin";
    if (!client) message.textContent = "Sign-in couldn’t load. Reload the page to try again.";
    renderAccount();
    if (!dialog.open) dialog.showModal();
    focusFirstField();
  }

  function setSync(state, text) {
    syncState = state;
    ui["sync-status"].textContent = text;
    ui["sync-status"].dataset.state = state;
    ui["account-button"].title = text;
    renderAccountButton();
  }

  function setBusy(busy) {
    submit.disabled = busy;
    submit.classList.toggle("busy", busy);
    form.setAttribute("aria-busy", String(busy));
  }

  function queueSync(delay = 200) {
    clearTimeout(syncTimer);
    if (!profile) return;
    if (!navigator.onLine) {
      setSync("offline", "Offline. Progress will sync when you reconnect.");
      return;
    }
    if (profile.syncing && delay < 30_000) {
      profile.syncAgain = true;
    } else {
      syncTimer = setTimeout(sync, delay);
    }
  }

  async function sync() {
    const current = profile;
    if (!current) return;
    if (current.syncing) {
      current.syncAgain = true;
      return;
    }
    current.syncing = true;
    setSync("syncing", "Syncing progress…");

    if (mergeProgress(progress, readProgress(current.storageKey))) onProgress(progress);
    const records = Array.from(progress, ([id, record]) => ({
      card_id: id, rating: record.rating, streak: record.streak, rated_at: record.ratedAt, due_at: record.dueAt,
    }));
    try {
      const { data, error } = await client.rpc("sync_flashcard_progress", {
        account_id: current.id,
        records,
      }).abortSignal(AbortSignal.timeout(10_000));
      if (error) throw error;
      if (profile !== current) return;

      const remote = new Map(data.map((row) => [row.card_id, {
        rating: row.rating, streak: row.streak, ratedAt: row.rated_at, dueAt: row.due_at,
      }]));
      if (mergeProgress(progress, remote, true)) {
        saveProgress(progress, current.storageKey);
        onProgress(progress);
      }

      const sentAt = Math.max(0, ...Array.from(activity.values(), (entry) => entry.at));
      const { data: days, error: activityError } = await client.rpc("sync_flashcard_activity", {
        account_id: current.id,
        device,
        records: toRows(activity, current.activitySentAt ?? 0),
      }).abortSignal(AbortSignal.timeout(10_000));
      if (activityError) throw activityError;
      if (profile !== current) return;
      current.activitySentAt = sentAt;
      const fromOthers = new Map();
      let restored = false;
      for (const row of days) {
        const entry = fromRow(row);
        if (!entry) continue;
        if (row.device_id === device) {
          // Days this browser uploaded before its local copy was cleared.
          const mine = activity.get(row.day);
          if (!mine || entry.at > mine.at) {
            activity.set(row.day, entry);
            restored = true;
          }
          continue;
        }
        if (!fromOthers.has(row.device_id)) fromOthers.set(row.device_id, new Map());
        fromOthers.get(row.device_id).set(row.day, entry);
      }
      others = fromOthers;
      saveOthers(others, current.othersKey);
      if (restored) saveActivity(activity, current.activityKey);
      onActivity();
      if (!current.syncAgain) setSync("synced", "Progress synced.");
    } catch {
      if (profile === current) {
        setSync("error", "Couldn’t sync. Trying again shortly.");
        queueSync(30_000);
      }
    } finally {
      current.syncing = false;
      if (current.syncAgain && current === profile) {
        current.syncAgain = false;
        queueSync(0);
      }
    }
  }

  function useSession(user) {
    if ((user?.id ?? null) !== (profile?.id ?? null)) {
      clearTimeout(syncTimer);
      const guest = readProgress();
      if (user) {
        profile = {
          id: user.id,
          email: user.email ?? "",
          storageKey: guestKey + "." + user.id,
          activityKey: activityKey + "." + user.id,
          othersKey: activityKey + ".others." + user.id,
        };
        const saved = readProgress(profile.storageKey);
        mergeProgress(saved, guest);
        progress = saved;
        saveProgress(progress, profile.storageKey);
        activity = readActivity(profile.activityKey);
        const guestDays = readActivity();
        if (guestDays.size) {
          addActivity(activity, guestDays);
          if (saveActivity(activity, profile.activityKey)) saveActivity(new Map());
        }
        others = readOthers(profile.othersKey);
        setSync("syncing", "Syncing progress…");
        queueSync(0);
      } else {
        profile = null;
        progress = guest;
        activity = readActivity();
        others = new Map();
        setSync("", "");
      }
      onProgress(progress, true);
      onActivity();
    }
    if (profile && user?.email) profile.email = user.email;
    renderAccount();
  }

  ui["account-button"].addEventListener("click", () => openAccount());
  ui["account-close"].addEventListener("click", () => dialog.close());
  ui["tab-signin"].addEventListener("click", () => view !== "signin" && setView("signin"));
  ui["tab-signup"].addEventListener("click", () => view !== "signup" && setView("signup"));
  ui["forgot-password"].addEventListener("click", () => setView("forgot"));
  ui["back-to-sign-in"].addEventListener("click", () => setView("signin"));
  ui["check-email-back"].addEventListener("click", () => setView("signin"));
  ui["reveal-password"].addEventListener("click", () => {
    const show = passwordInput.type === "password";
    passwordInput.type = show ? "text" : "password";
    ui["reveal-password"].setAttribute("aria-pressed", String(show));
    ui["reveal-password"].setAttribute("aria-label", show ? "Hide password" : "Show password");
  });
  dialog.addEventListener("close", () => {
    passwordInput.value = "";
    passwordInput.type = "password";
    ui["reveal-password"].setAttribute("aria-pressed", "false");
    ui["reveal-password"].setAttribute("aria-label", "Show password");
    if (view === "recovery" && !profile) view = "signin";
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!client || submit.disabled) return;
    const current = currentView();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    setBusy(true);
    message.textContent = "";
    try {
      if (current === "signin") {
        const { error } = await client.auth.signInWithPassword({ email, password });
        if (error) throw error;
        dialog.close();
        toast("Signed in. Your progress will sync.");
      } else if (current === "signup") {
        await createAccount(email, password);
        const { error } = await client.auth.signInWithPassword({ email, password });
        if (error) throw error;
        dialog.close();
        toast("Account created. You’re signed in.");
      } else if (current === "forgot") {
        const { error } = await client.auth.resetPasswordForEmail(email, { redirectTo });
        if (error) throw error;
        sentText = "If there’s an account for " + email + ", you’ll get a link to choose a new password.";
        setView("sent");
      } else if (current === "recovery") {
        const { error } = await client.auth.updateUser({ password });
        if (error) throw error;
        view = "signin";
        dialog.close();
        toast("Password updated.");
      }
    } catch (error) {
      message.textContent = errorMessage(error);
      form.classList.remove("shake");
      void form.offsetWidth;
      form.classList.add("shake");
    } finally {
      setBusy(false);
    }
  });

  ui["sign-out"].addEventListener("click", async () => {
    ui["sign-out"].disabled = true;
    try {
      const { error } = await client.auth.signOut({ scope: "local" });
      if (error) throw error;
      view = "signin";
      dialog.close();
      toast("Signed out. Progress stays saved in this browser.");
    } catch {
      setSync(syncState, "Couldn’t sign out. Please try again.");
    } finally {
      ui["sign-out"].disabled = false;
    }
  });

  window.addEventListener("online", () => queueSync(0));
  window.addEventListener("offline", () => profile && setSync("offline", "Offline. Progress will sync when you reconnect."));
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) queueSync(0);
  });
  window.addEventListener("storage", (event) => {
    const key = profile?.storageKey ?? guestKey;
    if (event.key === key && mergeProgress(progress, readProgress(key))) onProgress(progress);
    if (event.key === (profile?.activityKey ?? activityKey)) {
      activity = readActivity(event.key);
      onActivity();
    }
  });

  ui["google-sign-in"].addEventListener("click", async () => {
    if (!client || ui["google-sign-in"].disabled) return;
    ui["google-sign-in"].disabled = true;
    message.textContent = "";
    try { sessionStorage.setItem(oauthKey, "google"); } catch {}
    const { error } = await client.auth.signInWithOAuth({ provider: "google", options: { redirectTo } });
    if (error) {
      try { sessionStorage.removeItem(oauthKey); } catch {}
      message.textContent = "Google sign-in isn’t available right now. Use your email instead.";
      ui["google-sign-in"].disabled = false;
    }
  });
  if (client) {
    googleEnabled().then((enabled) => {
      google = enabled;
      renderAccount();
    });
  }

  if (client) {
    client.auth.onAuthStateChange((event, session) => {
      // Run outside the auth callback so Supabase calls made from here can't deadlock.
      setTimeout(() => {
        useSession(session?.user);
        if (event === "PASSWORD_RECOVERY") {
          callback.type = null;
          openAccount("recovery");
        } else if (event === "SIGNED_IN" && callback.type) {
          const messages = { signup: "Email confirmed. You’re signed in.", oauth: "Signed in with Google. Your progress will sync." };
          toast(messages[callback.type] ?? "You’re signed in.");
          callback.type = null;
        }
      });
    });
  }
  renderAccount();
  if (callback.error) {
    message.textContent = callback.error;
    openAccount("signin");
  }
  onProgress(progress);
  onActivity();

  return {
    rate(cardId, rating) {
      const key = profile?.storageKey ?? guestKey;
      mergeProgress(progress, readProgress(key));
      progress.set(cardId, rateProgress(progress.get(cardId), rating));
      const saved = saveProgress(progress, key);
      if (profile) {
        setSync("syncing", "Syncing progress…");
        queueSync();
      }
      return saved;
    },
    // Adds one answer to today's totals, with a snapshot of the box counts after it.
    logReview(correct, counts) {
      const key = profile?.activityKey ?? activityKey;
      recordReview(activity, correct, counts);
      saveActivity(activity, key);
      if (profile) queueSync();
      onActivity();
    },
    activity() {
      return combineActivity(activity, others);
    },
    signedIn() {
      return Boolean(profile);
    },
    // A fresh access token for the marking API, or null when signed out.
    async accessToken() {
      if (!client || !profile) return null;
      const { data } = await client.auth.getSession();
      return data.session?.access_token ?? null;
    },
    openSignIn() {
      openAccount("signin");
    },
  };
}
