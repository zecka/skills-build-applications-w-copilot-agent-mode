import { useCallback, useEffect, useMemo, useState } from 'react';

const codespaceName = process.env.REACT_APP_CODESPACE_NAME;
const baseUrl = codespaceName
  ? `https://${codespaceName}-8000.app.github.dev/api`
  : 'http://localhost:8000/api';
const endpoint = `${baseUrl}/teams/`;

function Teams() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filterText, setFilterText] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);

  const loadTeams = useCallback(async (signal) => {
    setLoading(true);
    setError('');

    try {
      console.log('Teams endpoint:', endpoint);
      const response = await fetch(endpoint, { signal });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      console.log('Teams fetched data:', data);

      const normalized = Array.isArray(data)
        ? data
        : Array.isArray(data?.results)
          ? data.results
          : [];

      setItems(normalized);
    } catch (requestError) {
      if (requestError.name !== 'AbortError') {
        setError(requestError.message || 'Failed to fetch teams');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    loadTeams(controller.signal);

    return () => controller.abort();
  }, [loadTeams]);

  const filteredItems = useMemo(() => {
    if (!filterText.trim()) {
      return items;
    }

    const query = filterText.toLowerCase();
    return items.filter((item) => JSON.stringify(item).toLowerCase().includes(query));
  }, [items, filterText]);

  const getRowSummary = (item) => {
    if (item?.name) return item.name;
    if (item?.title) return item.title;
    if (item?.username) return item.username;
    if (item?.email) return item.email;
    return 'Team record';
  };

  const getRowId = (item, index) => item?.id || item?._id || `row-${index + 1}`;

  return (
    <section className="card shadow-sm">
      <div className="card-body">
        <div className="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
          <h2 className="h3 mb-0">Teams</h2>
          <div className="d-flex align-items-center gap-2">
            <a className="link-primary link-offset-2" href={endpoint} target="_blank" rel="noreferrer">
              API Endpoint
            </a>
            <button
              type="button"
              className="btn btn-outline-primary btn-sm"
              onClick={() => loadTeams()}
            >
              Refresh
            </button>
          </div>
        </div>

        <form className="row g-2 mb-3" onSubmit={(event) => event.preventDefault()}>
          <div className="col-md-9">
            <input
              type="text"
              className="form-control"
              placeholder="Filter teams..."
              value={filterText}
              onChange={(event) => setFilterText(event.target.value)}
            />
          </div>
          <div className="col-md-3 d-grid">
            <button type="button" className="btn btn-secondary" onClick={() => setFilterText('')}>
              Clear Filter
            </button>
          </div>
        </form>

        {loading && <p className="text-body-secondary">Loading teams...</p>}
        {error && <p className="text-danger">Error: {error}</p>}

        {!loading && !error && (
          <div className="table-responsive">
            <table className="table table-striped table-hover align-middle mb-0">
              <thead className="table-light">
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">ID</th>
                  <th scope="col">Summary</th>
                  <th scope="col" className="text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredItems.map((item, index) => (
                  <tr key={getRowId(item, index)}>
                    <td>{index + 1}</td>
                    <td>{String(getRowId(item, index))}</td>
                    <td>{getRowSummary(item)}</td>
                    <td className="text-end">
                      <button
                        type="button"
                        className="btn btn-sm btn-primary"
                        onClick={() => setSelectedItem(item)}
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
                {filteredItems.length === 0 && (
                  <tr>
                    <td colSpan="4" className="text-center text-body-secondary">
                      No teams found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {selectedItem && (
        <>
          <div className="modal fade show d-block" tabIndex="-1" role="dialog" aria-modal="true">
            <div className="modal-dialog modal-lg modal-dialog-centered">
              <div className="modal-content">
                <div className="modal-header">
                  <h3 className="modal-title h5">Team Details</h3>
                  <button
                    type="button"
                    className="btn-close"
                    aria-label="Close"
                    onClick={() => setSelectedItem(null)}
                  />
                </div>
                <div className="modal-body">
                  <pre className="mb-0">{JSON.stringify(selectedItem, null, 2)}</pre>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setSelectedItem(null)}>
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="modal-backdrop fade show" onClick={() => setSelectedItem(null)} />
        </>
      )}
    </section>
  );
}

export default Teams;
