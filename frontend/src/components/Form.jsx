export default function Form({ children, onSubmit }) {
  return (
    <form onSubmit={onSubmit} className="max-w-md mx-auto bg-white p-6 rounded shadow mt-8">
      {children}
    </form>
  );
}
