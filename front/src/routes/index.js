import { createRouter, createWebHistory, createWebHashHistory } from "vue-router"
import routes from "./routers.js"
var router = createRouter({
    history: createWebHashHistory(),
    routes,
})

function getFirstRoute(){
    try{
        const data = JSON.parse(localStorage.getItem('chatweb'))
        return data.left_list[0].uuid
    }catch( e){
        return 1
    }
}

function hasRoute(uuid){
    try{
        var data = JSON.parse(localStorage.getItem('chatweb'))
    }catch( e){
        // localstorage 数据不存在
        if([1,2].indexOf(uuid) > -1){
            return true
        }
        return false
    }
    if(data !== null){

        const index = data.left_list.findIndex(v=>v.uuid == uuid)
        if(index > -1){
            return true
        }
        return false
    }else{
        return 1
    }
    
}

// to: 即将要进入的目标 用一种标准化的方式
// from: 当前导航正要离开的路由 用一种标准化的方式
router.beforeEach((to, from, next) => {
    // 若路由存在，则判断/chat/:uuid 是否存在
        // 若 localstorage 中 /chat/:uuid 不存在，则跳转到 第一个路由，
        // 否则就跳转到 /chat/:uuid
    // 路由不存在，则跳转到第一个路由
    console.log(to)
    if(to.matched.length > 0){
        // 路由存在
        if(to.name == 'chat'){
            var uuid = to.params.uuid
            if(hasRoute(uuid)){
                next()
            }else{
                router.push({name: 'chat', params:{uuid: getFirstRoute()}})
            }
        }else if(to.name == 'root'){

            router.push({name: 'chat', params:{uuid: getFirstRoute()}})
        }else{
            // 不是chat就继续
            next();
        }
    }else{
        // 路由不存在
        console.log('first route:', getFirstRoute())
        router.push({name: 'chat', params:{uuid: getFirstRoute()}})
    }

})

export default router