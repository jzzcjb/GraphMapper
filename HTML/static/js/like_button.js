'use strict';
// import React from 'react';
// import { Button, Space } from 'antd';

ReactDOM.render(
    <antd.Space wrap>
    <Button type="primary">Primary Button</Button>
    <Button>Default Button</Button>
    <Button type="dashed">Dashed Button</Button>
    <Button type="text">Text Button</Button>
    <Button type="link">Link Button</Button>
    </antd.Space>,
  document.getElementById("component-goes-here")
);
// function LikeButton() {
//   const [liked, setLiked] = React.useState(false);

//   if (liked) {
//     return 'You liked this!';
//   }

//   // return React.createElement(
//   //   'button',
//   //   {
//   //     onClick: () => setLiked(true),
//   //   },
//   //   'Like'
//   // );
//   return <button onClick={() => setLiked(true)}>Like</button>;
// }
// const domContainer = document.getElementById('component-goes-here');
// ReactDOM.render(React.createElement(LikeButton), domContainer);
// import React from 'react';
// import { Button, Space } from 'antd';
// const App = () => (
//   <Space wrap>
//     <Button type="primary">Primary Button</Button>
//     <Button>Default Button</Button>
//     <Button type="dashed">Dashed Button</Button>
//     <Button type="text">Text Button</Button>
//     <Button type="link">Link Button</Button>
//   </Space>
// );
// export default App;

// const domContainer = document.getElementById('component-goes-here');
// ReactDOM.render(React.createRoot.render(<App/>), domContainer);