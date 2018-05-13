import React, { Component } from 'react';
import './App.css';
import ListItem from './ListItem';
import Fetcher from './Fetch';

const backendAPI = process.env.REACT_APP_BACKEND_URL;

class UserSelectPage extends Component {
  onUserSelect = (data) => {
    console.log(`User ${data.user.username} clicked.`);
    this.props.advance(data);
  }

  render() {
    const Users = users => users.data.map((user, index) => <ListItem 
      name={user.user.first_name ? `${user.user.first_name} ${user.user.last_name}` : user.user.username}
      key={index}
      onClick={() => this.onUserSelect(user)}
    />);

    return (
      <div className="List">
        <Fetcher url={`${backendAPI}/userprofiles`}>
          <Users />
        </Fetcher>
      </div>
    );
  }
}

export default UserSelectPage;
