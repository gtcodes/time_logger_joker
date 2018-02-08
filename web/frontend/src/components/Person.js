import React, { Component } from 'react';

export class Person extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <p>{this.props.name} {this.props.email}</p>
        );
    }
}