import React, { Component } from 'react';
import './App.css';
import ListItem from './ListItem';
import Fetcher from './Fetch';

class UserSelectPage extends Component {
  onProductSelect = (data) => {
    console.log(`Product ${data.name} clicked.`);
    this.props.advance(data);
  }

  render() {
    const Products = products => products.data.map((product, index) => <ListItem 
      name={`${product.name} ${(product.price / 100.0).toFixed(2)}€`}
      key={index}
      onClick={() => this.onProductSelect(product)}
    />);

    return (
      <div className="List">
        <Fetcher url="http://localhost:8000/api/products">
          <Products />
        </Fetcher>
      </div>
    );
  }
}

export default UserSelectPage;
