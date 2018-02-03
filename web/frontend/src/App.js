import React, { Component } from 'react';
import { login } from './util/Auth';
import logo from './logo.svg';
import store from './store';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      token: null
    };
  }

  render() {
      const lIn = this.state.token;
      return (
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <h1 className="App-title">Welcome to React</h1>
          </header>
          <p className="App-intro">
            The user is logged in {lIn}
          </p>
        </div>
      );
  }
}

export default App;
