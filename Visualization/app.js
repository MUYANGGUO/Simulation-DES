/* global window */
import React, {Component} from 'react';
import {render} from 'react-dom';
import {StaticMap} from 'react-map-gl';
import {AmbientLight, PointLight, LightingEffect} from '@deck.gl/core';
import DeckGL from '@deck.gl/react';
// import {PolygonLayer} from '@deck.gl/layers';
import {PathLayer} from '@deck.gl/layers';
import {TripsLayer} from '@deck.gl/geo-layers';

// Set your mapbox token here
const MAPBOX_TOKEN = 'pk.eyJ1IjoibXV5YW5nZ3VvIiwiYSI6ImNrMnA0b3VrNTAwamgzZW55YTUwZHY4MngifQ.3--4_yqwizMxOLnxtu0QSQ'; // eslint-disable-line

// Source data CSV
const DATA_URL = {

  TRIPS:'./test.json'
};

const ambientLight = new AmbientLight({
  color: [255, 255, 255],
  intensity: 1.0
});

const pointLight = new PointLight({
  color: [255, 255, 255],
  intensity: 3.0,
  position: [-84.3888, 33.7769, 8000]
});

const lightingEffect = new LightingEffect({ambientLight, pointLight});

const material = {
  ambient: 0.1,
  diffuse: 0.6,
  shininess: 32,
  specularColor: [60, 64, 70]
};

const DEFAULT_THEME = {
//   buildingColor: [74, 80, 87],
//   trailColor0: [253, 128, 93],
//   trailColor1: [23, 184, 190],
  material,
  effects: [lightingEffect]
};

const INITIAL_VIEW_STATE = {
  longitude: -84.38883,
  latitude: 33.77687,
  zoom: 20,
  pitch: 45,
  bearing: 30
};


export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      time: 0
    };
  }

  componentDidMount() {
    this._animate();
  }

  componentWillUnmount() {
    if (this._animationFrame) {
      window.cancelAnimationFrame(this._animationFrame);
    }
  }

  _animate() {
    const {
      loopLength = 360, // unit corresponds to the timestamp in source data
      animationSpeed = 2 // unit time per second
    } = this.props;
    const timestamp = Date.now() / 1000;
    const loopTime = loopLength / animationSpeed;

    this.setState({
      time: ((timestamp % loopTime) / loopTime) * loopLength
    });
    this._animationFrame = window.requestAnimationFrame(this._animate.bind(this));
  }

  _renderLayers() {
    const {
      trips = DATA_URL.TRIPS,
      trailLength = 500,
      theme = DEFAULT_THEME
    } = this.props;

    return [
      // This is only needed when using shadow effects
      new TripsLayer({
        id: 'trips',
        data: trips,
        getPath: d => d.path,
        getTimestamps: d => d.timestamps,
        // getColor: d => (d.vendor === 0 ? theme.trailColor0 : theme.trailColor1),
        getColor: function(d){ 
            if (d.lane <= 3.0) 
            return [255,102,102]; 
            else if(d.lane == 4.0) 
            return [178,255,102];
            else if (d.lane == 5.0)
            return [102,255,255]; 
            else if (d.lane == 6.0 || d.lane == 7.0)
            return [255,153,153];
            else if (d.lane==8.0)
            return [153,255,153];
            else if (d.lane == 9.0)
            return [153,153,255];
            else 
            return [255,255,153];
              },
        opacity: 1,
        widthMinPixels: 1,
        rounded: true,
        trailLength: 2,
        currentTime: this.state.time,
        shadowEnabled: false
      })
    ];
  }

  render() {
    const {
      viewState,
      mapStyle = 'mapbox://styles/mapbox/dark-v9',
      theme = DEFAULT_THEME
    } = this.props;

    return (
      <DeckGL
        layers={this._renderLayers()}
        effects={theme.effects}
        initialViewState={INITIAL_VIEW_STATE}
        viewState={viewState}
        controller={true}
      >
        <StaticMap
          reuseMaps
          mapStyle={mapStyle}
          preventStyleDiffing={true}
          mapboxApiAccessToken={MAPBOX_TOKEN}
        />
      </DeckGL>
    );
  }
}

export function renderToDOM(container) {
  render(<App />, container);
}