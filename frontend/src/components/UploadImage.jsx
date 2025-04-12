import React, { useState } from 'react';
import api from '../api';

const UploadImage = ({ setProductInfo }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Por favor selecciona una imagen.');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await api.post('/scan_barcode/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const productData = response.data;

      // Crear un objeto con los datos de la respuesta
      const product = {
        barcode: productData.barcode,
        name: productData.data[2],  // el nombre está en el segundo campo de 'data'
        labelImage: `http://localhost:8000/labels/${productData.label_image.split("\\").pop()}`, // Crear la URL de la imagen
      };

      setProductInfo(product);  // Actualiza la UI con los datos del producto
    } catch (err) {
      setError('Error al procesar la imagen. Inténtalo de nuevo.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2 className="title">Escáner de código de barras</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Procesando...' : 'Subir Imagen'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default UploadImage;