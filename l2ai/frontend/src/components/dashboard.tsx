import React, { useState } from "react";

import "../styleSheets/styles.css";
import TextField from "./fields/textField";
import AsyncButton from "./buttons/asyncButton";


const Dashboard: React.FC = () => {
  const [text, setText] = useState("");

  return (
    <div className="column grow align-center">
      <div>
        <h1>MyMaum</h1>
      </div>
      <div className="flex w100p">
        <div className="grow column p2 w50p h800">
          <div className="grow mb1">
            <TextField
              className={"font-l"}
              type={"textarea"}
              placeholder={"Paste your content here..."}
              onKeyup={setText}
            />
          </div>
          <div className="justify-center">
            <AsyncButton
              onClick={async () => console.log("Click")}
              children={<span className="font-l">Start learning</span>}
              type="primary"
              size="xlarge"
            />
          </div>
        </div>
        <div className="grow p2 w50p h800">
          <span>Feedback area</span>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
