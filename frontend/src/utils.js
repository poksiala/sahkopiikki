import { toast } from 'react-toastify';

const popup = (text, level) => {
  toast[level](text, {
    position: toast.POSITION.BOTTOM_CENTER,
    autoClose: 6000,
  });
}

export {
  popup,
};