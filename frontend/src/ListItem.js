import React, { Component } from 'react';
import classNames from 'classnames';

const ListItem = props => (
  <div {...props} className={classNames([props.className, 'ListItem'])}>
    { props.name }
  </div>
);

export default ListItem;