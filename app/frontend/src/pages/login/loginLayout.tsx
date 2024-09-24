import { Outlet } from "react-router-dom";
import NavBarNoMenu from "../../components/navBar/navBarNoMenu";


/**
 * The React Router layout for all children of the login component.
 */
const LoginLayout = () => {
  return (
    <main className="flex flex-col h-screen">
      <NavBarNoMenu />
      <div className="flex flex-grow items-center justify-center">
          <Outlet />
      </div>
    </main>
  );
};


export default LoginLayout;
