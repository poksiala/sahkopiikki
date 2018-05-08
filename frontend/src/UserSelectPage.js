import React, { Component } from 'react';
import './App.css';
import ListItem from './ListItem';

const ukkelit = [
  'Panu',
  'Jan',
  'A-J',
  'Eero',
  'Jan',
  'A-J',
  'Eero',
  'Jan',
  'A-J',
  'Eero',
  'Jan',
  'A-J',
  'Eero',
  'Jan',
  'A-J',
  'Eero',

];

class UserSelectPage extends Component {
  onUserSelect = (data) => {
    console.log(`User ${data} clicked.`);
    this.props.advance(data);
  }

  render() {
    return (
      <div className="List">
        { ukkelit.map((ukkeli, index) => <ListItem 
            name={ukkeli}
            key={index}
            onClick={() => this.onUserSelect(ukkeli)}
          />)
        }
      </div>
    );
  }
}

export default UserSelectPage;
