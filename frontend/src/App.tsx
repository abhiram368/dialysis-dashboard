import CreateSession from "./components/CreateSession";
import SessionList from "./components/SessionList";

function App() {
  return (
    <div>
      <h1>Dialysis Dashboard</h1>
      <CreateSession />
      <SessionList />
    </div>
  );
}

export default App;