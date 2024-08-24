<template>
    <div v-if="centerLodding" class=" absolute top-1/3 left-1/3 bg-gray w-1/3 h1/3 flex justify-center items-center ">
        <n-spin size="large" />
    </div>
    <div class=" flex flex-row h-min ">
        <!-- 非移动端的侧边栏的样式 -->
        <div class=" sm:w-1/5 h-full  " :class="controlSidebarHidden ? 'w-0' : ''">
            <div class="hidden sm:flex sm:flex-col sm:h-screen sm:border ">
                <!-- 新建按钮 -->
                <div class=" basis-1/12   flex justify-center items-center">
                    <n-button class="w-4/5 dark:text-white" @click="addLeftListEle">+ New Chat</n-button>
                </div>
                <!-- 列表 -->

                <div class="basis-10/12  overflow-auto border  ">

                    <div v-for=" item in left_data.left_list" :key="item.uuid">
                        <!-- 侧边栏输入框 -->
                        <router-link :to="`/chat/${item.uuid}`" class="m-2 flex flex-row justify-between items-center 
                        border border-gray-400  rounded-md p-2  dark:text-white">

                            <div class=" w-4/5 flex items-center">
                                <n-icon size="medium">
                                    <game-controller-outline />
                                </n-icon>
                                <div class=" truncate mx-2">
                                    <p v-if="!item.enable_edit" class=" truncate h-full">{{ item.title }}</p>
                                    <n-input v-else type="text" size="small" class=" h-full " :hidden="false"
                                        v-model:value="item.title" @keyup.enter="submit(item.uuid)"></n-input>
                                </div>
                            </div>
                            <div class="w-1/5 flex justify-center items-center "
                                :class="route.params.uuid != item.uuid ? 'hidden' : ''">
                                <n-button-group size="small" :vertical="false" :hidden="false">
                                    <n-button text size="" @click="editLeftListEle(item.uuid)">
                                        <n-icon>
                                            <Edit />
                                        </n-icon>
                                    </n-button>
                                    <n-button text @click="delLeftListEle(item.uuid)">
                                        <n-icon>
                                            <Delete />
                                        </n-icon>
                                    </n-button>

                                </n-button-group>
                            </div>
                        </router-link>
                    </div>


                </div>
                <!-- 设置页面 -->
                <div class="basis-1/12 flex justify-start items-center h-full  ">
                    <!-- 头像 -->

                    <div class=" w-1/4  flex justify-center items-center" @click="handleAvatarClick()">
                        <n-tooltip trigger="hover">
                            <template #trigger>
                                <img class=" rounded-full h-10 w-10" :src="avatar" alt="avatar">
                            </template>
                            点击修改头像
                        </n-tooltip>
                    </div>
                    <input type="file" ref="avatarInput" style="display: none;" @change="handleAvatarChange"
                        accept="image/*" />
                    <!-- 简介 -->
                    <div class=" w-2/4  h-full grid grid-rows-2">
                        <div class=" flex justify-start items-end font-bold">
                            算命大师
                        </div>
                        <div class=" text-xs">
                            Start On <a class=" text-blue-400"
                                href="https://github.com/gzhuuser/fortune_teller">Github</a>
                        </div>
                    </div>
                    <!-- 设置 -->
                    <div class=" w-1/4  h-full flex justify-center items-center">
                        <n-icon @click="showSettingFunc()">
                            <SettingsOutline></SettingsOutline>
                        </n-icon>
                        <!-- 设置 modal -->
                        <div
                            class="hidden absolute top-0 left-0 bg-transparent  w-screen h-screen border border-red-200">
                            <div class=" flex justify-center items-center">
                                <n-modal v-model:show="showSetting" style="width: 600px" class="custom-card"
                                    preset="card" title="" size="huge">

                                    <template #header-extra>
                                    </template>
                                    <n-tabs type="line" animated>
                                        <n-tab-pane name="about" tab="关于">
                                            <div>这是一个给定非惯用手的图片进行识别和命运分析的“算命大师”网站</div>
                                            <div class="my-4">技术栈：Vue3 + Vite + tailwindCss3 + NaiveUi</div>
                                            <div class="my-4">多模态识别 + RAG + 浪潮llm</div>
                                            <div class="my-4">前端：Vue3 + Vite + tailwindCss3 + NaiveUi</div>
                                            <div class="my-4">后端：python + flask</div>
                                        </n-tab-pane>
                                        <n-tab-pane name="other" tab="开发文档">
                                            开发文档：<a
                                                href="https://rvg7j9czg8m.feishu.cn/wiki/HcFMwY0zviaaXHkvZa8cH9fYnmf">点击跳转
                                            </a>
                                        </n-tab-pane>
                                    </n-tabs>

                                </n-modal>
                            </div>

                        </div>
                    </div>

                </div>
            </div>
        </div>
        <!-- 移动端模式下侧边栏的样式 -->
        <div class=" sm:hidden absolute top-1 left-1  h-full w-full flex flex-col ">
            <div>
                <n-button text style="font-size:32px" key="" @click="controlSidebarHidden = !controlSidebarHidden">
                    <n-icon class=" text-black dark:text-white">
                        <Menu></Menu>
                    </n-icon>
                </n-button>
            </div>
            <div v-if="!controlSidebarHidden" class=" w-4/5 sm:hidden bg-white dark:bg-black">
                <div class=" w-full flex  flex-col  h-screen border ">
                    <!-- 新建按钮 -->
                    <div class=" basis-1/12   flex justify-center items-center  ">
                        <n-button class="w-4/5 dark:text-white" @click="addLeftListEle">+ New Chat</n-button>
                    </div>
                    <!-- 列表 -->

                    <div class="basis-10/12  overflow-auto border  ">

                        <div v-for=" item in left_data.left_list" :key="item.uuid">
                            <!-- 侧边栏输入框 -->
                            <router-link :to="`/chat/${item.uuid}`" class="m-2 flex flex-row justify-between items-center 
                        border border-gray-400  rounded-md p-2  dark:text-white ">

                                <div class=" w-4/5 flex items-center ">
                                    <n-icon size="medium">
                                        <game-controller-outline />
                                    </n-icon>
                                    <div class=" truncate mx-2">
                                        <p v-if="!item.enable_edit" class=" truncate h-full">{{ item.title }}</p>
                                        <n-input v-else type="text" size="small" class=" h-full " :hidden="false"
                                            v-model:value="item.title" @keyup.enter="submit(item.uuid)"></n-input>
                                    </div>
                                </div>
                                <div class="w-1/5 flex justify-center items-center "
                                    :class="route.params.uuid != item.uuid ? 'hidden' : ''">
                                    <n-button-group size="small" :vertical="false" :hidden="false">
                                        <n-button text size="" @click="editLeftListEle(item.uuid)">
                                            <n-icon>
                                                <Edit />
                                            </n-icon>
                                        </n-button>
                                        <n-button text @click="delLeftListEle(item.uuid)">
                                            <n-icon>
                                                <Delete />
                                            </n-icon>
                                        </n-button>

                                    </n-button-group>
                                </div>
                            </router-link>
                        </div>


                    </div>
                    <!-- 设置页面 -->
                    <div class="basis-1/12 flex justify-start items-center h-full  ">
                        <!-- 头像 -->
                        <div class=" w-1/4  flex justify-center items-center" @click="handleAvatarClick()">
                            <img class=" rounded-full h-10 w-10" :src="avatar" alt="avatar">
                        </div>
                        <input type="file" ref="avatarInput" style="display: none;" @change="handleAvatarChange"
                            accept="image/*" />

                        <!-- 简介 -->
                        <div class=" w-2/4  h-full grid grid-rows-2">
                            <div class=" flex justify-start items-end font-bold">
                                用户
                            </div>
                            <div class=" text-xs">
                                我们的项目地址：Start On <a class=" text-blue-400"
                                    href="https://github.com/gzhuuser/fortune_teller">Github</a>
                            </div>
                        </div>
                        <!-- 设置 -->
                        <div class=" w-1/4  h-full flex justify-center items-center">
                            <n-icon @click="showSettingFunc()">
                                <SettingsOutline></SettingsOutline>
                            </n-icon>
                            <!-- 设置 modal -->
                            <div
                                class="hidden absolute top-0 left-0 bg-transparent  w-screen h-screen border border-red-200">
                                <div class=" flex justify-center items-center">
                                    <n-modal v-model:show="showSetting" style="width: 600px" class="custom-card"
                                        preset="card" title="" size="huge">

                                        <template #header-extra>
                                        </template>
                                        <n-tabs type="line" animated>
                                            <n-tab-pane name="about" tab="关于">
                                                <div>这是一个给定非惯用手的图片进行识别和命运分析的“算命大师”网站</div>
                                                <div class="my-4">技术栈：Vue3 + Vite + tailwindCss3 + NaiveUi</div>
                                                <div class="my-4">多模态识别 + RAG + 浪潮llm</div>
                                                <div class="my-4">前端：Vue3 + Vite + tailwindCss3 + NaiveUi</div>
                                                <div class="my-4">后端：python + flask</div>
                                            </n-tab-pane>
                                            <n-tab-pane name="other" tab="开发文档">
                                                开发文档：<a
                                                    href="https://rvg7j9czg8m.feishu.cn/wiki/HcFMwY0zviaaXHkvZa8cH9fYnmf">点击跳转
                                                </a>
                                            </n-tab-pane>
                                        </n-tabs>

                                    </n-modal>
                                </div>

                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>

        <div class="w-full  sm:w-4/5 h-full  ">
            <div class="flex flex-col h-screen ">
                <!-- 这里是IM区域 -->
                <div class=" basis-11/12 w-full p-12 overflow-auto container" id="msgArea">
                    <div v-for="(msglist, index) in getMsgList(route.params.uuid)" :key="index"
                        class=" flex flex-col mt-1  msgItem ">
                        <div :class="msglist.reversion ? 'flex-row-reverse' : 'flex-row'"
                            class=" flex justify-start items-center h-10">
                            <img class=" rounded-full h-10 w-10" :src="msglist.reversion ? avatar : '/assets/icon.jpg'"
                                alt="avatar">
                            <span class="ml-4 text-sm">{{ msglist.create_time }}</span>
                        </div>
                        <div class="flex  " :class="msglist.reversion ? 'flex-row-reverse' : 'flex-row'">
                            <div
                                class="bg-blue-200 dark:bg-white dark:text-black w-auto max-w-[80%] min-w-[1%] break-words overflow-ellipsis rounded-sm p-2 my-1">
                                <img :src="msglist.image" v-if="msglist.image"
                                    style="max-width: 200px;max-height: 200px;" alt="手相图">

                                <Markdown :source="msglist.text"></Markdown>
                            </div>

                        </div>
                    </div>


                </div>
                <div class=" basis-1/12   w-full">
                    <!-- 这里是输入框 -->
                    <div class="  p-2">
                        <n-input-group>
                            <n-tooltip trigger="hover">
                                <template #trigger>
                                    <n-button text size="large" class="px-2"
                                        @click="deleteChatItemHistory(route.params.uuid)">
                                        <n-icon class=" text-black dark:text-white">
                                            <Delete></Delete>
                                        </n-icon>
                                    </n-button>
                                </template>
                                删除当前会话记录
                            </n-tooltip>
                            <n-tooltip trigger="hover">
                                <template #trigger>
                                    <n-button text size="large" class=" pr-4" @click="dom2img()">
                                        <n-icon class=" text-black dark:text-white">
                                            <Download></Download>
                                        </n-icon>
                                    </n-button>
                                </template>
                                下载当前会话为图片
                            </n-tooltip>
                            <div>
                                <div style="display: flex;">
                                    <div class=" mr-4" style="    margin-top:8px; color:grey">来算一卦吧（请选择你要分析的手相）：
                                    </div>
                                    <n-tooltip trigger="hover">
                                        <template #trigger>
                                            <n-select style=" width: 200px ;margin-top:4px;" :options="selectOptions"
                                                v-model:value="Input_feature" />

                                        </template>
                                        <img class="hand" />
                                    </n-tooltip>

                                    <n-button ghost class=" h-auto dark:text-blue " style="margin-top:4px;"
                                        @click="showFeatureFunc()">
                                        选好了~
                                    </n-button>
                                </div>
                            </div>

                        </n-input-group>
                        <n-modal style="width: 1000px" class="custom-card" preset="card" v-model:show="showFeature"
                            title="" size="huge">
                            <div class="table">
                                <ul class="table-row-group">
                                    <li v-for="(detail, index) in details" :key="index" class="table-item">
                                        <label>
                                            <input type="checkbox" :value="detail.id" v-model="selected_details" />
                                            <img :src="detail.image" alt="Detail Image" class="table-image" />
                                            {{ detail.name }}
                                        </label>
                                    </li>
                                </ul>
                            </div>
                            <n-button @click="updateTextArea">选好了，开始算命吧~</n-button>
                        </n-modal>

                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import detailData from '@/assets/detailsData.json';
import {
    NButton, NInput, NIcon, NButtonGroup, NSpin,
    NInputGroup, NCard, NModal, NTabs, NTabPane, NInputNumber, NSelect,
    NTooltip,
    useMessage,
    create
} from 'naive-ui'
import { GameControllerOutline, GameController } from '@vicons/ionicons5'
import { LogInOutline as LogInIcon, SettingsOutline, Menu } from '@vicons/ionicons5'
import { Edit, Delete, Download, Upload } from '@vicons/carbon'
import Markdown from 'vue3-markdown-it';

import { reactive, ref, getCurrentInstance, watch, watchEffect, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router'
import html2canvas from "html2canvas";


const router = useRouter()
const route = useRoute()
const instaceV = getCurrentInstance()
const message = useMessage()
const fileInput = ref(null);
const selectedImage = ref(null);
const showHand = ref(false);
const showFeature = ref(false);
const showSetting = ref(false)
const avatar = ref('../assets/human5.png');
const avatarInput = ref(null);
const Input_feature = ref(null);
const details = ref([]);
const selected_details = ref([]);
const selectOptions = ref([
    // '感情线','生命线','智慧线','婚姻线','事业线'
    {
        label: '感情线',
        value: '感情线'
    },
    {
        label: '生命线',
        value: '生命线'
    },
    {
        label: '智慧线',
        value: '智慧线'
    },
    {
        label: '婚姻线',
        value: '婚姻线'
    },
    {
        label: '事业线',
        value: '事业线'
    }
])
const input_text_area = ref(null)
const detailsData = detailData.detailData
const loadDetails = () => {
    // 根据选择的input_feature加载details
    // console.log(Input_feature.value,detailsData,detailsData[Input_feature.value])
    //   console.log(detailData)
    details.value = detailsData[Input_feature.value] || [];
    selected_details.value = []; // 重置已选择的详情
    // input_text_area.value = ''; // 清空文本区域 

}

const updateTextArea = () => {
    // 将选中的details添加到input_text_area
    const selectedNames = details.value
        .filter(detail => selected_details.value.includes(detail.id))
        .map(detail => detail.name)
        .join(', ');
    input_text_area.value = selectedNames;
    console.log(input_text_area.value, selectedNames)
    if(input_text_area.value === ''){
        message.error('请先选择你的手相特征')
    }else{
        addMessageListItem(route.params.uuid);
        showFeature.value = !showFeature.value;
    }
    
}
const handleAvatarClick = () => {
    // console.log(avatar.value)
    avatarInput.value.click();
}

const handleAvatarChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            avatar.value = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};
// 控制侧边栏显示隐藏
var controlSidebarHidden = ref(true)

var centerLodding = ref(false)

// var input_area_value = ref('')
var left_data = reactive({
    left_list: [
        { uuid: 1, title: 'New Chat1', enable_edit: false },
        // { uuid: 2, title: 'New Chat2', enable_edit: false },
    ],
    chat: [
        {
            uuid: 1, msg_list: [
                { image: null, text: 'hello,我是算命大师，欢迎来到我的网站，请上传你的手相图并向我咨询吧~', feature: '', create_time: (new Date()).toLocaleString('sv-SE', { "timeZone": "PRC" }), reversion: false, msgload: false },
                // { type: 'text',content: 'hallo', create_time: '2024-8-15 12:00:00', reversion: true, msgload: true}
            ]
        },

    ],

})

const handleUploadImage = () => {
    fileInput.value.click();
}
const image_url = (image) => {
    console.log(image)
    return new FileReader().readAsDataURL(image);
}
const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            selectedImage.value = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

// 监听响应式数据
watch(left_data, (newValue, oldValue) => {
    // TODO:待完善，只能存储5m，多了会报错，后期可以改成存在后端数据库然后从后端中获取
    localStorage.setItem('chatweb', JSON.stringify(newValue))
})


// 创建响应式变量后只执行一次输出的需求
watchEffect(() => {
    // 读取 localstorage
    const data = localStorage.getItem('chatweb')
    if (data) {
        const history = JSON.parse(data)
        left_data.left_list = history.left_list
        left_data.chat = history.chat
    }
})


// 添加侧壁栏item
function addLeftListEle() {
    const uuid = randomUuid()
    left_data.left_list.push({
        uuid: uuid,
        title: `New Chat${uuid}`,
        enable_edit: false
    })
    left_data.chat.push({
        uuid: uuid,
        msg_list: [
            { image: null, text: 'hello,我是算命大师，欢迎来到我的网站，请向我咨询吧~', feature: '', create_time: (new Date()).toLocaleString('sv-SE', { "timeZone": "PRC" }), reversion: false, msgload: false },
        ]
    })

    // 路由跳转到最新的item
    router.push({ name: 'chat', params: { uuid: uuid } })

}
// 点击侧边栏某个item的编辑按钮
function editLeftListEle(uuid) {
    const index = left_data.left_list.findIndex(v => v.uuid == uuid)
    left_data.left_list[index].enable_edit = !left_data.left_list[index].enable_edit

    // all_data.left_list[index].enable_edit = !all_data.left_list[index].enable_edit
    // ls.updateLeftListItemEnableEditButton(uuid)

}

// 点击侧边栏某个item的删除按钮
function delLeftListEle(uuid) {
    var index = left_data.left_list.findIndex(v => v.uuid == uuid)
    left_data.left_list.splice(index, 1)
}

// 获取每个 chat 的msg list
function getMsgList(uuid) {
    if (uuid && uuid != undefined) {
        var index = left_data.chat.findIndex(v => v.uuid == uuid)
        // console.log(left_data.chat,uuid)
        return left_data.chat[index].msg_list
    }
    return []

}

function randomUuid() {
    var len = 9
    var uuid = '';
    for (let i = 0; i < len; i++) {
        uuid += Math.floor(Math.random() * 10)
    }
    return Number(uuid, 10)
}

// 监听侧边栏item的回车事件
function submit(index) {
    editLeftListEle(index)

}

// 发送消息
function showHandFcn() {

    if (input_area_value.value === '') {
        message.error('请输入内容')
    }
    else {
        showHand.value = !showHand.value
    }
}
function showFeatureFunc(uuid) {
    if (Input_feature.value == null) {
        message.error('请先选择你想要分析的手相线')
    } else {
        showFeature.value = !showFeature.value;
        this.loadDetails();
    }
}
function addMessageListItem(uuid) {
    console.log(input_text_area.value)
    // console.log(Input_feature.value)
    if (Input_feature.value != null) {
        // showHandFcn()
        // console.log(Input_feature)
        var index = left_data.chat.findIndex(v => v.uuid == uuid)
        const now_t = (new Date()).toLocaleString('sv-SE', { "timeZone": "PRC" })
        if (input_text_area.value) {
            left_data.chat[index].msg_list.push({
                // type: 'text',
                // image:null,
                text: input_text_area.value,
                feature: Input_feature.value,
                create_time: now_t,
                reversion: true,
                msgload: false
            })
            startStream(index)
            input_text_area.value = ''
        }


        var ele = document.getElementById("msgArea")
        ele.scrollTop = ele.scrollHeight + ele.offsetHeight
        left_data.chat[index].msg_list.push({
            // image:null,
            text: '',
            feature: '',
            create_time: now_t,
            reversion: false,
            msgload: true
        })

    } else {
        message.error('请先选择你要分析的手相线~')
    }

}

async function startStream(index) {
    const requestData = {
        text: left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].text,
        // image: image.split(',')[1],  // 仅发送Base64部分
        feature: left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].feature
    };
    console.log(JSON.stringify(requestData))
    fetch("http://localhost:9000/v3", {
        "method": "POST",
        "headers": {
            'Content-Type': 'application/json;charset=utf-8'
        },
        "mode": "cors",
        "body": JSON.stringify(requestData),
        "timeout": 3000,
    })
        .then(response => {
            if (response.status !== 200) {
                // console.log(response)
                left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].text += `发生了一些错误：${response.status}-${response.statusText}\n后台小哥哥正在维修~`
                return false
            }
            left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].msgload = false
            console.log(response)
            // if (response.status !== 200) {
            //     left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].text += `发生了一些错误：${response.status}-${response.statusText}`
            //     return false
            // }

            const reader = response.body.getReader();
            let buffer = ''; // 用于缓存数据块

            const readStream = async () => {
                const { done, value } = await reader.read();
                if (done) {
                    console.log('Stream reading complete');
                    return;
                }

                const chunk = new TextDecoder('utf-8').decode(value);
                left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].text += chunk
                return readStream();
            }

            // 开始处理流数据
            return readStream();

        }).
        catch(error => {
            if (error.message === 'fail to fetch')
                left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].text += '发生了一些错误：${error.message}\n后台小哥哥正在维修~'
            return false
        });


};







function showSettingFunc() {
    console.log(123)
    showSetting.value = !showSetting.value
}

// 删除当前会话记录
function deleteChatItemHistory(uuid) {
    const index = left_data.chat.findIndex(v => v.uuid == uuid);
    left_data.chat[index].msg_list = []
    message.success('当前会话记录已清理')
}

// 当前会话下载为图片
async function dom2img() {
    centerLodding.value = true

    var ele = document.querySelectorAll(".msgItem")
    var msgAreaDom = document.getElementById("msgArea")

    const width = msgAreaDom.offsetWidth * 2
    const height = msgAreaDom.scrollHeight * 1.5


    let canvas1 = document.createElement('canvas');
    let context = canvas1.getContext('2d');
    canvas1.width = width;
    canvas1.height = height;
    // 绘制矩形添加白色背景色
    context.rect(0, 0, width, height);
    context.fillStyle = "#fff";
    context.fill();

    let beforeHeight = 0
    for (let i = 0; i < ele.length; i++) {
        const dom_canvas = await html2canvas(ele[i], {
            scrollX: 0,
            scrollY: 0,
            height: ele[i].scrollHeight,
            width: ele[i].scrollWidth,
        })

        // var image = dom_canvas.toDataURL("image/png");
        context.drawImage(dom_canvas, 0, beforeHeight, dom_canvas.width, dom_canvas.height)
        beforeHeight = beforeHeight + dom_canvas.height;

    }
    var image = canvas1.toDataURL("image/png").replace("image/png", "image/octet-stream");
    var link = document.getElementById("link");
    link.setAttribute("download", `chatweb-${(new Date()).getTime()}.png`);
    link.setAttribute("href", image);
    link.click();

    centerLodding.value = false
    message.success('图片下载完成')

}


</script>


<style scoped>
.container {
    background-image: url('/assets/bg.jpg');
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;

}

.hand {
    width: 600px;
    height: 600px;
    background-image: url('/assets/手相.jpg');
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
}

.router-link-active {
    border-color: #18a058;
    color: #18a058;
}

.table {
    display: table;
    width: 100%;
    height: 500px;
    overflow-y: auto;
    table-layout: fixed;
    /* 固定表格布局 */
}

.table-row-group {
    display: table-row-group;
}

.table-item {
    display: table-cell;
    width: 20%;
    /* 设置每行四个项目 */
    padding: 8px;
    height: auto;
    text-align: center;
    /* 文本居中对齐示例 */
    box-sizing: border-box;
    /* 边框计算在宽度内 */
}

.table-image {
    max-width: 100%;
    /* 确保图片宽度不超过单元格宽度 */
    height: auto;
}

/* 仅用于展示的额外样式 */
.table-row-group {
    margin: 0;
    padding: 0;
}

.table-item {
    list-style-type: none;
    display: inline-block;
    /* 也可以使用 inline-block 来实现每行四个项目 */
    vertical-align: top;
}
</style>
