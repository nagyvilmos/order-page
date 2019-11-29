import React from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { withRouter } from "react-router";

import Loading from "./view/Loading";
import { getData } from "./worker";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loaded: false,
      data: undefined
    };
  }

  componentDidMount() {
    // if (!this.loaded) {
    //   getData({});
    // }
  }

  componentDidUpdate() {
    // stuff happened in the app
  }

  render() {
    if (!this.state.loaded) {
      return <Loading />;
    }

    return (
      <div>
        <h1
          style={{
            padding: "16px",
            marginBottom: "16px",
            color: "cyan",
            backgroundColor: "darkcyan"
          }}
        >
          Silly Playground
        </h1>
        <div
          style={{
            border: "solid",
            borderWidth: "8px",
            borderColor: "darkcyan",
            padding: "4px"
          }}
        >
          <h2>Updated</h2>
          <p style={{ margin: "16px" }}>
            Lorem, ipsum dolor sit amet consectetur adipisicing elit.
            Dignissimos veniam debitis ea officia molestias enim odit, in eaque
            esse obcaecati? Consequuntur aliquid est aperiam fugiat culpa
            tempora! Eum, ipsa porro.
          </p>
          <p style={{ margin: "16px" }}>
            Lorem, ipsum dolor sit amet consectetur adipisicing elit.
            Dignissimos veniam debitis ea officia molestias enim odit, in eaque
            esse obcaecati? Consequuntur aliquid est aperiam fugiat culpa
            tempora! Eum, ipsa porro.
          </p>
          <footer>tis the end</footer>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state, currentProps) => {
  return { loaded: true };
};

const mapDispatchToProps = dispatch =>
  bindActionCreators(
    {
      getData: getData
    },
    dispatch
  );

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(App));
