import { logout } from '../utils/auth';

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between">
      <div className="font-bold">SMPS</div>
      <button onClick={logout}>Logout</button>
    </nav>
  );
}
