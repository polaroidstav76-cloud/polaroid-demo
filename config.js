// Демо-копия сайта: своя база Supabase с выдуманными данными, рабочая база сюда не подключена.
const SUPABASE_URL = 'https://mautbgsvpafzirkawbrh.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_wo9Y33fkUT9uwl6YzutO0A_JpPhcFF_';

// Логин сотрудника превращается во внутренний адрес вида login@STAFF_EMAIL_DOMAIN (писем туда не отправляем).
const STAFF_EMAIL_DOMAIN = 'staff.polaroid.local';
// true — без входа сайт не открывается.
const STAFF_LOGIN_REQUIRED = true;

// Полоса «Демо-версия» вверху страницы.
document.addEventListener('DOMContentLoaded', () => {
  const bar = document.createElement('div');
  bar.textContent = 'Демо-версия: все клиенты, продажи и отчёты здесь выдуманные';
  bar.style.cssText = 'background:#fef3c7;color:#92400e;text-align:center;font:600 13px/1.4 system-ui,sans-serif;padding:6px 12px;border-bottom:1px solid #fcd34d';
  document.body.prepend(bar);
});
