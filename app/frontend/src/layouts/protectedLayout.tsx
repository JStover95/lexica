import { Outlet } from "react-router-dom";
import NavBar from "../components/navBar/navBarMobile";


/**
 * The React Router layout for all children of the login component.
 */
const ProtectedLayout = () => {
  return (
    <main className="flex flex-col h-screen">
      <NavBar />
      <div className="flex flex-grow items-center justify-center">
          <Outlet />
      </div>
    </main>
  );
};


export default ProtectedLayout;
