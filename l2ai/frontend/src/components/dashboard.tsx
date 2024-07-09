import * as React from 'react';
import "./dashboard.css"

export interface IDashboardProps {
}

export interface IDashboardState {
}

class Dashboard extends React.Component<IDashboardProps, IDashboardState> {
  state = {}

  public render() {
    const {} = this.props;

    return (
      <div>
        <p>MyMaum</p>
      </div>
    );
  }
}

export default Dashboard;
