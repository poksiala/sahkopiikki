import React, { Component } from 'react';
import './App.css';
import ListItem from './ListItem';

const products = [
  'Karuh A',
  'Sol',
  'Pääkkis',
  'Panusafka',
  'Teline',
];

class UserSelectPage extends Component {
  onProductSelect = (data) => {
    console.log(`Product ${data} clicked.`);
    this.props.advance(data);
  }

  render() {
    return (
      <div className="List">
        { products.map((product, index) => <ListItem 
            name={product}
            key={index}
            onClick={() => this.onProductSelect(product)}
          />)
        }
      </div>
    );
  }
}

export default UserSelectPage;
