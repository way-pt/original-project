import React from "react";
import PropTypes from "prop-types";
const MapView = ({ data }) =>

    <div className="column">
        <div className="generated-image card mb-3">
        <div className="row no-gutters image-card">
            <div className="col-md-10 img-container">
                <img src={data.image} className="card-img" alt="{data.image}"></img>
            </div>
            <div className="col-md-2 bg-dark image-sidebar">
                <div className="card-body text-light image-view-tree">
                    <h5 className="map-name text-right border-bottom border-secondary">{data.name}</h5>
                    <p className="map-user text-right">{data.user_username}</p>
                    <p className="map-date text-right border-bottom border-secondary"><small className="text-muted">{data.date}</small></p>
                    <p className="map-data-title text-right">Data files</p>
                    <p className="map-data text-right">{data.data_file}</p>
                </div>
            </div>
        </div>
    </div>
    </div>

MapView.propTypes = {
  data: PropTypes.object.isRequired
};

  export default MapView;
