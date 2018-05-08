import React, { Component } from 'react';
import './App.css';
import ListItem from './ListItem';

class UserSelectPage extends Component {
  onConfirm = () => {
    console.log(`Confirmed.`);
    this.props.advance(true);
  }

  onReject = () => {
    console.log('Rejected!');
    this.props.advance(false);
  }

  render() {
    const { user, product } = this.props.info;
    return (
      <div className="List">
        <div className="Summary-row">
          <label>Nimi: </label>{ user }
        </div>
        <div className="Summary-row">
          <label>Tuote: </label>{ product }
        </div>
        <ListItem className="Success" name="Hyväksy" onClick={() => this.onConfirm()} />
        <ListItem className="Danger" name="Peruuta ja palaa alkuun" onClick={() => this.onReject()} />
      </div>
    );
  }
}

export default UserSelectPage;
