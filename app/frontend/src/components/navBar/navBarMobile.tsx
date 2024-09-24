import React, { createRef, useState } from "react";
import MenuIcon from '@mui/icons-material/Menu';
import { NavLink } from "react-router-dom";
import CloseIcon from '@mui/icons-material/Close';


const NavBar: React.FC = () => {
  const [drawerOpen, setDrawerOpen] = useState(true);
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

  const drawer =
    <div ref={drawerRef} className="flex flex-col bg-white z-10 shadow-xl absolute w-full top-[80px] h-[292px] overflow-hidden transition-all duration-500">
      <div className="py-4 px-8">
        <NavLink
          to="/"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " btn-primary rounded-4xl" : "")
          }}>
            Read
        </NavLink>
        <NavLink
          to="/create"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " btn-primary rounded-4xl" : "")
          }}>
            Create
        </NavLink>
        <NavLink
          to="/review"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " btn-primary rounded-4xl" : "")
          }}>
            Review
        </NavLink>
        <NavLink
          to="/account"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " btn-primary rounded-4xl" : "")
          }}>
            Account
        </NavLink>
        <NavLink
          to="/logout"
          end
          className={({ isActive }) => {
            return "btn justify-start px-8 py-3 text-lg" + (isActive ? " btn-primary rounded-4xl" : "")
          }}>
            Log Out
        </NavLink>
      </div>
    </div>

  return (
    <>
      <div className="flex items-center justify-between w-screen h-[80px] px-8 shadow-lg">
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
