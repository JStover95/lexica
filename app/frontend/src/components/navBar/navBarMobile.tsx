import React, { createRef, useState } from "react";
import MenuIcon from '@mui/icons-material/Menu';
import { NavLink } from "react-router-dom";
import CloseIcon from '@mui/icons-material/Close';


const NavBar: React.FC = () => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const drawerRef = createRef<HTMLDivElement>();

  const handleClickMenu = () => {
    if (drawerRef.current) {
      drawerRef.current.style.height = "292px";
      setDrawerOpen(true);
    }
  }

  const handleClickCloseMenu = () => {
    if (drawerRef.current) {
      drawerRef.current.style.height = "0px";
      setDrawerOpen(false);
    }
  }

  // TODO: Come back and move nav links to a component
  const drawer =
    <div ref={drawerRef} className="flex-col bg-white z-50 shadow-xl w-full fixed top-[80px] h-[0px] overflow-hidden transition-all duration-500 webkit-overflow-scrolling">
      <div className="py-4 px-8">
        <NavLink
          to="/"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " text-primary" : "")
          }}>
            Read
        </NavLink>
        <NavLink
          to="/create"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " text-primary" : "")
          }}>
            Create
        </NavLink>
        <NavLink
          to="/review"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " text-primary" : "")
          }}>
            Review
        </NavLink>
        <NavLink
          to="/account"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " text-primary" : "")
          }}>
            Account
        </NavLink>
        <NavLink
          to="/logout"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " text-primary" : "")
          }}>
            Log Out
        </NavLink>
      </div>
    </div>

  return (
    <>
      <div className="flex flex-shrink-0 items-center justify-between w-screen h-[80px] px-8 sticky top-0 z-40 bg-white shadow-lg">
        <h1 className="text-4xl font-bold">Lexica</h1>
        {
          drawerOpen ?
          <div
            onClick={handleClickCloseMenu}
            className="flex items-center justify-center cursor-pointer h-[60px] w-[60px] cursor-pointer">
            <CloseIcon fontSize="large" />
          </div> :
          <div
            onClick={handleClickMenu}
            className="flex items-center justify-center cursor-pointer h-[60px] w-[60px] cursor-pointer">
            <MenuIcon fontSize="large"/>
          </div>
        }
      </div>
      {drawer}
    </>
  );
};


export default NavBar;
