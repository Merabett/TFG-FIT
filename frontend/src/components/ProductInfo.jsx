import React, { useState } from 'react';

const ProductInfo = ({ product }) => {
  const [modalOpen, setModalOpen] = useState(false);

  if (!product) return null;

  const handleImageClick = () => {
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
  };

  return (
    <div className="product-info-container">
      <h2>Información del Producto</h2>
      {product.error ? (
        <p style={{ color: 'red' }}>❌ {product.error}</p>
      ) : (
        <div>
          <p><strong>Código de barras:</strong> {product.barcode}</p>
          <p><strong>Nombre:</strong> {product.name}</p>
          {/* Mostrar la imagen de la etiqueta nutricional */}
          {product.labelImage && (
            <div>
              <h3>Etiqueta Nutricional:</h3>
              <img 
                src={product.labelImage} 
                alt="Etiqueta Nutricional" 
                className="label-image" 
                onClick={handleImageClick} 
              />
              {/* Modal para imagen ampliada */}
              {modalOpen && (
                <div className="modal" onClick={closeModal}>
                  <div className="modal-content">
                    <img 
                      src={product.labelImage} 
                      alt="Etiqueta Nutricional Ampliada" 
                      className="modal-image" 
                    />
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ProductInfo;