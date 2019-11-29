import React, { Component } from "react";
import Body from "./Body";
import { LoadingWrapper } from "../components/styledComponents";

export default class Loading extends Component {
  render() {
    return (
      <Body>
        <LoadingWrapper>
          <h1>Loading...</h1>
        </LoadingWrapper>
      </Body>
    );
  }
}
