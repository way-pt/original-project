import React from "react";
import PropTypes from "prop-types";

const ListItems = ({ data, onClick }) => data.map((i) => 
<li className="media border border-lightgrey shadow-sm" onClick={onClick} key={i.pk}>
    <img src={i.image} className="mr-3 map-list-image align-self-center" alt="..."></img>
    <div className="media-body">
        <h5 className="mt-0 mb-1"><a href='#' className='map-link'  onClick={onClick} data-pk={i.pk}>{i.name}</a></h5>
        {i.username} | added on {i.date}
</div></li>
)
ListItems.propTypes = {
    data: PropTypes.array.isRequired,
    onClick: PropTypes.func.isRequired
}

const MapList = ({ data, onClick }) =>

    <ul className="list-unstyled"><ListItems data={data} onClick={onClick} /></ul>

MapList.propTypes = {
    data: PropTypes.array.isRequired,
    onClick: PropTypes.func.isRequired
};
export default MapList;
