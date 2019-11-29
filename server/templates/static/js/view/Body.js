import React, { Component } from "react";
import Header from "../components/Header";

export default class Body extends Component {
  render() {
    const { children } = this.props;

    return (
      <div>
        <Header />
        <div
          style={{
            border: "solid",
            borderWidth: "8px",
            borderColor: "darkcyan",
            padding: "4px"
          }}
        >
          {children}
        </div>
      </div>
    );
  }
}
