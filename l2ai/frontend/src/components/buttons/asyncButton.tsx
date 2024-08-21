import React, { useState } from "react";

interface AsyncButtonProps {
  onClick: () => Promise<any>;
  text: string;
  type: string;
}

const AsyncButton: React.FC<AsyncButtonProps> = ({ onClick, text, type }) => {
  const [loading, setLoading] = useState<boolean>(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      await onClick();
    } finally {
      setLoading(false);
    }
  };

  const loader = (
    <div className="lds-ring lds-ring-small">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
  );

  return (
    <button
      className={`button button-large button-${type}`}
      onClick={handleClick}
      disabled={loading}
    >
      {loading ? loader : text}
    </button>
  );
};

export default AsyncButton;
