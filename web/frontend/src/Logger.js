import React, { Component } from 'react';
import { Router } from 'react-router-dom';
import { apiClient } from './util/ApiClient';
import axios from 'axios';
import { Person } from './components/Person';

export class Logger extends Component {

    constructor(props) {
        super(props);
        this.state = {
            attendees: null,
            api: apiClient()
        };
        this.get_api_attendees();
    }

    get_api_attendees() {
        return this.state.api.get("/users.json")
            .then((resp) => {
                console.log(resp.data);
                this.setState({attendees: resp.data});
            })
            .catch((e) => {
                console.log(e);
            });
    }

    render() {
        const attendees = this.state.attendees;
        var renderThis = [];
        if (attendees) {
            for (var i = 0; i < attendees.length; i++){
                renderThis.push(<Person key={i} name={attendees[i].username} email={attendees[i].email}/>);
            }
        }
        return (
            <div>
                <h1>Logger</h1>
                <p> it works!</p>
                {renderThis}
            </div>
        );
    }
}
