import React, { Component } from 'react';
import './App.css';
import ListItem from './ListItem';
import Fetcher from './Fetch';

class UserSelectPage extends Component {
  onUserSelect = (data) => {
    console.log(`User ${data} clicked.`);
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
        <Fetcher url="http://localhost:8000/api/userprofiles">
          <Users />
        </Fetcher>
      </div>
    );
  }
}

export default UserSelectPage;
