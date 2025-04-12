import React, { useState } from 'react';
import UploadImage from './components/UploadImage';
import ProductInfo from './components/ProductInfo';
import './App.css';

const App = () => {
  const [productInfo, setProductInfo] = useState(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Escáner de Código de Barras</h1>
      </header>
      <main>
        <UploadImage setProductInfo={setProductInfo} />
        <ProductInfo product={productInfo} />
      </main>
    </div>
  );
};

export default App;
