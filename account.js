import { guestKey, readProgress, saveProgress, rateProgress, mergeProgress } from "./progress.js?v=1";

const apiUrl = "https://mosmevfnxnnxxmmktfcb.supabase.co";
const publishableKey = "sb_publishable_B2CkIOCAUSm_uEg7nN7rAQ_MPAI7XU4";
const loginEmail = "study@maths-flashcards.example";

export function connectAccount(ui, onProgress) {
  const dialog = ui["account-dialog"];
  const form = ui["sign-in-form"];
  const passwordInput = ui["account-password"];
  const message = ui["account-message"];
  const client = window.supabase?.createClient(apiUrl, publishableKey, {
    auth: { detectSessionInUrl: false, storageKey: "maths-flashcards.session.v1" },
  });
  let progress = readProgress();
  let profile = null;
  let setupToken = new URLSearchParams(location.hash.slice(1)).get("setup");
  let syncTimer;

  if (setupToken) history.replaceState(history.state, "", location.pathname + location.search);

  function settingPassword() {
    return Boolean(setupToken || profile?.needsPassword);
  }

  function renderAccount() {
    const setup = settingPassword();
    ui["account-button"].textContent = profile ? "Account" : "Sign in";
    ui["account-title"].textContent = setup ? "Set your password" : profile ? "Your account" : "Sign in";
    ui["account-intro"].textContent = setup
      ? "Choose a password with at least 12 characters. You’ll use it on each device."
      : "Sync your flashcard progress across your devices.";
    form.hidden = Boolean(profile) && !setup;
    ui["signed-in-panel"].hidden = !profile || setup;
    ui["sign-in-submit"].textContent = setup ? "Set password" : "Sign in";
    passwordInput.minLength = setup ? 12 : 1;
    passwordInput.autocomplete = setup ? "new-password" : "current-password";
  }

  function openAccount() {
    message.textContent = client ? "" : "Sign-in couldn’t load. Reload to try again.";
    renderAccount();
    if (!dialog.open) dialog.showModal();
    (form.hidden ? ui["account-close"] : passwordInput).focus();
  }

  function syncStatus(text) {
    ui["sync-status"].textContent = text;
    ui["account-button"].title = text;
  }

  function queueSync(delay = 200) {
    clearTimeout(syncTimer);
    if (!profile) return;
    if (!navigator.onLine) {
      syncStatus("Waiting for a connection to sync.");
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
    syncStatus("Syncing progress…");

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
      if (!current.syncAgain) syncStatus("Progress synced.");
    } catch {
      if (profile === current) {
        syncStatus("Couldn’t sync. Your browser will try again.");
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
        profile = { id: user.id, storageKey: guestKey + "." + user.id };
        const saved = readProgress(profile.storageKey);
        mergeProgress(saved, guest);
        progress = saved;
        saveProgress(progress, profile.storageKey);
        syncStatus("Syncing progress…");
        queueSync(0);
      } else {
        profile = null;
        progress = guest;
        syncStatus("");
      }
      onProgress(progress, true);
    }
    if (profile) profile.needsPassword = user.user_metadata?.flashcards_setup === true;
    renderAccount();
    if (settingPassword() && !dialog.open) openAccount();
  }

  ui["account-button"].addEventListener("click", openAccount);
  dialog.addEventListener("close", () => { passwordInput.value = ""; });
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!client || ui["sign-in-submit"].disabled) return;
    const password = passwordInput.value;
    ui["sign-in-submit"].disabled = true;
    message.textContent = "";
    try {
      if (settingPassword()) {
        if (setupToken) {
          const { error } = await client.auth.verifyOtp({ token_hash: setupToken, type: "invite" });
          if (error) throw error;
          setupToken = null;
        }
        const { error } = await client.auth.updateUser({ password, data: { flashcards_setup: false } });
        if (error) throw error;
      } else {
        const { error } = await client.auth.signInWithPassword({ email: loginEmail, password });
        if (error) throw error;
      }
      dialog.close();
    } catch (error) {
      if (error.code === "otp_expired") {
        setupToken = null;
        renderAccount();
        message.textContent = "This setup link has expired or has already been used.";
      } else if (error.code === "invalid_credentials") {
        message.textContent = "That password didn’t work.";
      } else if (error.code === "weak_password") {
        message.textContent = "Choose a stronger password.";
      } else if (error.status === 429) {
        message.textContent = "Too many attempts. Wait a minute and try again.";
      } else {
        message.textContent = "Couldn’t connect. Please try again.";
      }
    } finally {
      ui["sign-in-submit"].disabled = false;
    }
  });

  ui["sign-out"].addEventListener("click", async () => {
    ui["sign-out"].disabled = true;
    try {
      const { error } = await client.auth.signOut({ scope: "local" });
      if (error) throw error;
      dialog.close();
    } catch {
      message.textContent = "Couldn’t sign out. Please try again.";
    } finally {
      ui["sign-out"].disabled = false;
    }
  });
  window.addEventListener("online", () => queueSync(0));
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) queueSync(0);
  });
  window.addEventListener("storage", (event) => {
    const key = profile?.storageKey ?? guestKey;
    if (event.key === key && mergeProgress(progress, readProgress(key))) onProgress(progress);
  });
  if (client) client.auth.onAuthStateChange((_event, session) => useSession(session?.user));
  else renderAccount();
  if (setupToken) openAccount();
  onProgress(progress);

  return {
    rate(cardId, rating) {
      const key = profile?.storageKey ?? guestKey;
      mergeProgress(progress, readProgress(key));
      progress.set(cardId, rateProgress(progress.get(cardId), rating));
      const saved = saveProgress(progress, key);
      if (profile) {
        syncStatus("Syncing progress…");
        queueSync();
      }
      return saved;
    },
  };
}
