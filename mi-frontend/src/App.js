import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [token, setToken] = useState('');
  const [libros, setLibros] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');
  const [filtroAutor, setFiltroAutor] = useState('');
  const [filtroAnio, setFiltroAnio] = useState('');
  const [search, setSearch] = useState('');
  const [ordering, setOrdering] = useState('');
  const [page, setPage] = useState(1);
  const [formLibro, setFormLibro] = useState({ titulo: '', autor: '', anio: '', isbn: '' });
  const [editId, setEditId] = useState(null);

  // Login y obtención del token
  const login = async (e) => {
    e.preventDefault();
    try {
      const resp = await axios.post('http://localhost:8000/token/', {
        username,
        password
      });
      setToken(resp.data.access);
      setMsg('Login exitoso');
    } catch (err) {
      setMsg('Login incorrecto');
    }
  };

  // Logout
  const logout = () => {
    setToken('');
    setLibros([]);
    setMsg('Sesión cerrada');
  };

  // Obtener libros con filtros, paginación y orden
  const getLibros = async () => {
    let url = `http://localhost:8000/libros/?page=${page}`;
    if (filtroAutor) url += `&autor=${encodeURIComponent(filtroAutor)}`;
    if (filtroAnio) url += `&anio=${encodeURIComponent(filtroAnio)}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;
    if (ordering) url += `&ordering=${ordering}`;
    try {
      const resp = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLibros(resp.data.results || resp.data);
      setMsg('Libros cargados');
    } catch (err) {
      setMsg('No autorizado o error en la API');
    }
  };

  // Crear o editar libro
  const guardarLibro = async (e) => {
    e.preventDefault();
    try {
      if (editId) {
        await axios.put(`http://localhost:8000/libros/${editId}/`, formLibro, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setMsg('Libro editado');
      } else {
        await axios.post('http://localhost:8000/libros/', formLibro, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setMsg('Libro creado');
      }
      setFormLibro({ titulo: '', autor: '', anio: '', isbn: '' });
      setEditId(null);
      getLibros();
    } catch (err) {
      setMsg('Error al guardar libro');
    }
  };

  // Eliminar libro
  const eliminarLibro = async (id) => {
    if (!window.confirm('¿Eliminar este libro?')) return;
    try {
      await axios.delete(`http://localhost:8000/libros/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMsg('Libro eliminado');
      getLibros();
    } catch (err) {
      setMsg('Error al eliminar libro');
    }
  };

  // Preparar edición
  const editarLibro = (libro) => {
    setFormLibro({
      titulo: libro.titulo,
      autor: libro.autor,
      anio: libro.anio,
      isbn: libro.isbn
    });
    setEditId(libro.id);
  };

  // Cargar libros al cambiar filtros/paginación/orden
  useEffect(() => {
    if (token) getLibros();
    // eslint-disable-next-line
  }, [token, filtroAutor, filtroAnio, search, ordering, page]);

  return (
    <div style={{ padding: '2rem', maxWidth: 700 }}>
      <h2>Demo Django + React + JWT</h2>
      {!token ? (
        <form onSubmit={login} style={{ marginBottom: '1rem' }}>
          <input
            type="text"
            placeholder="Usuario"
            value={username}
            onChange={e => setUsername(e.target.value)}
            style={{ marginRight: '0.5rem' }}
          />
          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{ marginRight: '0.5rem' }}
          />
          <button type="submit">Login</button>
        </form>
      ) : (
        <div style={{ marginBottom: '1rem' }}>
          <button onClick={logout}>Logout</button>
        </div>
      )}
      <div style={{ marginBottom: '1rem', color: 'green' }}>{msg}</div>
      {token && (
        <>
          <div style={{ marginBottom: '1rem' }}>
            <input
              type="text"
              placeholder="Filtrar por autor"
              value={filtroAutor}
              onChange={e => setFiltroAutor(e.target.value)}
              style={{ marginRight: '0.5rem' }}
            />
            <input
              type="number"
              placeholder="Filtrar por año"
              value={filtroAnio}
              onChange={e => setFiltroAnio(e.target.value)}
              style={{ marginRight: '0.5rem' }}
            />
            <input
              type="text"
              placeholder="Buscar texto"
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{ marginRight: '0.5rem' }}
            />
            <select value={ordering} onChange={e => setOrdering(e.target.value)}>
              <option value="">Ordenar por...</option>
              <option value="anio">Año ascendente</option>
              <option value="-anio">Año descendente</option>
              <option value="autor">Autor ascendente</option>
              <option value="-autor">Autor descendente</option>
            </select>
            <button onClick={() => setPage(1)} style={{ marginLeft: '0.5rem' }}>Buscar</button>
          </div>
          <form onSubmit={guardarLibro} style={{ marginBottom: '1rem' }}>
            <input
              type="text"
              placeholder="Título"
              value={formLibro.titulo}
              onChange={e => setFormLibro({ ...formLibro, titulo: e.target.value })}
              required
              style={{ marginRight: '0.5rem' }}
            />
            <input
              type="text"
              placeholder="Autor"
              value={formLibro.autor}
              onChange={e => setFormLibro({ ...formLibro, autor: e.target.value })}
              required
              style={{ marginRight: '0.5rem' }}
            />
            <input
              type="number"
              placeholder="Año"
              value={formLibro.anio}
              onChange={e => setFormLibro({ ...formLibro, anio: e.target.value })}
              required
              style={{ marginRight: '0.5rem' }}
            />
            <input
              type="text"
              placeholder="ISBN"
              value={formLibro.isbn}
              onChange={e => setFormLibro({ ...formLibro, isbn: e.target.value })}
              required
              style={{ marginRight: '0.5rem' }}
            />
            <button type="submit">{editId ? 'Editar' : 'Crear'} Libro</button>
            {editId && (
              <button type="button" onClick={() => { setEditId(null); setFormLibro({ titulo: '', autor: '', anio: '', isbn: '' }); }} style={{ marginLeft: '0.5rem' }}>Cancelar</button>
            )}
          </form>
          <ul style={{ marginTop: '2rem' }}>
            {libros.map(libro => (
              <li key={libro.id}>
                <b>{libro.titulo}</b> - {libro.autor} ({libro.anio}) [ISBN: {libro.isbn}]
                <button onClick={() => editarLibro(libro)} style={{ marginLeft: '1rem' }}>Editar</button>
                <button onClick={() => eliminarLibro(libro.id)} style={{ marginLeft: '0.5rem' }}>Eliminar</button>
              </li>
            ))}
          </ul>
          <div style={{ marginTop: '2rem' }}>
            <button onClick={() => setPage(page > 1 ? page - 1 : 1)} disabled={page === 1}>Anterior</button>
            <span style={{ margin: '0 1rem' }}>Página {page}</span>
            <button onClick={() => setPage(page + 1)}>Siguiente</button>
          </div>
        </>
      )}
    </div>
  );
}

export default App;