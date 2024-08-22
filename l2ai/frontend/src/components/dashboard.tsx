import React from "react";

import "../styleSheets/styles.css";


const Dashboard: React.FC = () => {
  return (
    <div className="column grow align-center">
      <div>
        <h1>MyMaum</h1>
      </div>
      <div className="flex wfull">
        <div className="grow p2">
          <span>Text area</span>
        </div>
        <div className="grow p2">
          <span>Feedback area</span>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
