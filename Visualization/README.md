## installation guide:

```bash
# cd to the Visualization folder
cd ../Simulation-DES/Visualization
# install dependencies using node.js
npm install
```

## run:

After getting the test.json from running simulator.py in the upper level directory, cd to Visualization directory, and run the following command:

```bash
npm start
```
The localhost will be started, and a web browser with the visualization page will be shown up. 

## Animation speed setting:

The animation cycle time, looplenth should be based on your simulation time duration (unit: second). 
If you run the simulation over 1 hour, you should set this number at least 3600. 

The animation speed is the scaled up playback speedup. You can set any number to increase the time lapse speed for playback.

In app.js line 75. 

```javascript
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
```

