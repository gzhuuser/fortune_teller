var routes = [
  {path: "/",template: "<div>这里是根路由</div>", name: 'root'},
  {path: "/chat/:uuid", template: "这里是 /chat/:uuid", name:'chat'},
  {path: "/404",template: "这里是404"},

];
export default routes;
