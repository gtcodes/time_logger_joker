import React, { Component } from 'react';
import { login } from './util/Auth';
import logo from './logo.svg';
import store from './store';
import './App.css';
import { Login } from './Login';
import { Logger } from './Logger';
import { Route, Switch } from 'react-router-dom';

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
          <div>
            <Switch>
              <Route exact path="/" render={() => <h1>Home</h1>} />
              <Route path="/today" component={Logger} />
              <Route path="/login" component={Login} />
            </Switch>
          </div>
      );
  }
}

export default App;
