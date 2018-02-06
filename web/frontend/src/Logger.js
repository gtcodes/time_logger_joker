import React, { Component } from 'react';
import { Router } from 'react-router-dom';
import { apiClient } from './util/ApiClient';
import axios from 'axios';

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
                console.log("response got");
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
            console.log(attendees.keys());
            for (var i = 0; i < attendees.length; i++){
                console.log(i);
                renderThis.push(<h2 key={i}>{attendees[i].username}</h2>);
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
// att man lånar ord är naturligt då grupper oftast delas upp i yrkesgrupper och andra subgrupper. 
// Gamers -> blandad med engelska. 
// Stora gruppen kommer i kontakt med andra språk medan liten grupp isolerar sig