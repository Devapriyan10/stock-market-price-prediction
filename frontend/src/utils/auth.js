export function setToken(t) {
  localStorage.setItem('token', t);
}
export function getToken() {
  return localStorage.getItem('token');
}
export function authHeader() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}
export function logout() {
  localStorage.removeItem('token');
  window.location.href = '/login';
}
