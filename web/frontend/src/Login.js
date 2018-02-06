import React, { Component } from 'react';
import apiclient from './util/ApiClient';
import { login } from './util/Auth';
import { Router } from 'react-router-dom';
import store from './store'

export class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    handleSubmit(event) {
        console.log("loggin' in!");
        return login(this.state.username, this.state.password)
            .then(() => {
                // Router.transitionTo("/logger");
                console.log(this.store.getState().token)
            });
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Name:
                    <input name="username" type="text" value={this.state.username} onChange={this.handleChange} />
                </label>
                <label>
                    Password:
                    <input name="password" type="password" value={this.state.password} onChange={this.handleChange} />
                </label>
            <input type="submit" value="Submit" />
          </form>
        );
    }
}
