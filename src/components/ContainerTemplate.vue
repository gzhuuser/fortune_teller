<template>
    <div v-if="centerLodding" class=" absolute top-1/3 left-1/3 bg-gray w-1/3 h1/3 flex justify-center items-center ">
        <n-spin size="large" />
    </div>
    <div class=" flex flex-row h-min " >
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
                            <img class=" rounded-full h-10 w-10" :src=" avatar " alt="avatar">
                    </div>
                    <input type="file" ref="avatarInput" style="display: none;" @change="handleAvatarChange" accept="image/*" />
                    <!-- 简介 -->
                    <div class=" w-2/4  h-full grid grid-rows-2">
                        <div class=" flex justify-start items-end font-bold">
                            算命大师
                        </div>
                        <div class=" text-xs">
                            Start On <a class=" text-blue-400" href="https://github.com/gzhuuser/fortune_teller">Github</a>
                        </div>
                    </div>
                    <!-- 设置 -->
                    <div class=" w-1/4  h-full flex justify-center items-center">
                        <n-icon @click="showSettingFunc()">
                            <SettingsOutline></SettingsOutline>
                        </n-icon>
                        <!-- 设置 modal -->
                        <div class="hidden absolute top-0 left-0 bg-transparent  w-screen h-screen border border-red-200">
                            <div class=" flex justify-center items-center">
                                <n-modal v-model:show="showSetting" style="width: 600px" class="custom-card" preset="card"
                                    title="" size="huge">

                                    <template #header-extra>
                                    </template>
                                    <n-tabs type="line" animated>
                                        <n-tab-pane name="about" tab="关于">
                                            <div>这是一个demo项目，仅用于学习。</div>
                                            <div class="my-4">技术栈：Vue3 + Vite + tailwindCss3 + NaiveUi</div>
                                        </n-tab-pane>
                                        <n-tab-pane name="settings" tab="设置">
                                            <div class=" grid grid-rows-3 gap-4">
                                                <div>
                                                    <span class=" mr-4">Model: </span>
                                                    <n-select :style="{ width: '80%' }" :options="selectOptions"
                                                        v-model:value="setting.model" />
                                                </div>
                                                <div>
                                                    <span class=" mr-4">Temperatures: </span>
                                                    <n-input-number :style="{ width: '80%' }" :default-value="0.8"
                                                        :step="0.1" :max="1" :min="0.1"
                                                        v-model:value="setting.Temperatures" />
                                                </div>
                                                <div>
                                                    <span class=" mr-4">Top_p: </span>
                                                    <n-input-number :style="{ width: '80%' }" :default-value="1" :step="1"
                                                        :max="1" :min="1" v-model:value="setting.Top_p" />
                                                </div>
                                            </div>
                                        </n-tab-pane>
                                        <n-tab-pane name="other" tab="开发文档">
                                            开发文档：
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
            <div  >
                <n-button text style="font-size:32px"  key=""  @click="controlSidebarHidden=!controlSidebarHidden" >
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
                            <img class=" rounded-full h-10 w-10" :src=" avatar " alt="avatar">
                        </div>
                        <input type="file" ref="avatarInput" style="display: none;" @change="handleAvatarChange" accept="image/*" />

                        <!-- 简介 -->
                        <div class=" w-2/4  h-full grid grid-rows-2">
                            <div class=" flex justify-start items-end font-bold">
                                算命大师
                            </div>
                            <div class=" text-xs">
                                Start On <a class=" text-blue-400" href="https://github.com/gzhuuser/fortune_teller">Github</a>
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
                                                <div>这是一个demo项目，仅用于学习。</div>
                                                <div class="my-4">技术栈：Vue3 + Vite + tailwindCss3 + NaiveUi</div>
                                            </n-tab-pane>
                                            <n-tab-pane name="settings" tab="设置">
                                                <div class=" grid grid-rows-3 gap-4">
                                                    <div>
                                                        <span class=" mr-4">Model: </span>
                                                        <n-select :style="{ width: '80%' }" :options="selectOptions"
                                                            v-model:value="setting.model" />
                                                    </div>
                                                    <div>
                                                        <span class=" mr-4">Temperatures: </span>
                                                        <n-input-number :style="{ width: '80%' }" :default-value="0.8"
                                                            :step="0.1" :max="1" :min="0.1"
                                                            v-model:value="setting.Temperatures" />
                                                    </div>
                                                    <div>
                                                        <span class=" mr-4">Top_p: </span>
                                                        <n-input-number :style="{ width: '80%' }" :default-value="1"
                                                            :step="1" :max="1" :min="1" v-model:value="setting.Top_p" />
                                                    </div>
                                                </div>
                                            </n-tab-pane>
                                            <n-tab-pane name="other" tab="其他">
                                                其他
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
                <div class=" basis-11/12 w-full p-12 overflow-auto container" id="msgArea" >
                    <div v-for="(msglist, index) in getMsgList(route.params.uuid)" :key="index"
                        class=" flex flex-col mt-1  msgItem ">
                        <div :class="msglist.reversion ? 'flex-row-reverse' : 'flex-row'"
                            class=" flex justify-start items-center h-10">
                            <img class=" rounded-full h-10 w-10"  :src="msglist.reversion?'/assets/human5.png':'/assets/icon.jpg'" alt="avatar">
                            <span class="ml-4 text-sm">{{ msglist.create_time }}</span>
                        </div>
                        <div class="flex  " :class="msglist.reversion ? 'flex-row-reverse' : 'flex-row'">
                            <div
                                class="bg-blue-200 dark:bg-white dark:text-black w-auto max-w-[80%] min-w-[1%] break-words overflow-ellipsis rounded-sm p-2 my-1">
                                <n-spin v-if="msglist.msgload" size="small" stroke="red" />
                                <Markdown v-else :source="msglist.content"></Markdown>
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
                            <a href="" id="link" class="hidden"></a>
                            <n-tooltip trigger="hover">
                                <template #trigger>
                                    <n-button text size="large" class=" pr-4" @click="handleUploadImage()">
                                        <n-icon class=" text-black dark:text-white">
                                            <Upload></Upload>
                                        </n-icon>
                                    </n-button>
                                </template>
                                上传手相图片
                            </n-tooltip>

                            <input type="file" ref="fileInput" style="display: none;" @change="handleFileChange" accept="image/*" />
                            <n-input show-count @keyup.ctrl.enter="addMessageListItem(route.params.uuid)"
                                placeholder="请输入你的问题" v-model:value="input_area_value" type="textarea" size="tiny" :autosize="{
                                    minRows: 2,
                                    maxRows: 5
                                }" >
                                 <template #suffix>
                                    <img v-if="selectedImage" :src="selectedImage" alt="Selected Image" class="max-h-20 max-w-20" />
                                 </template>
                            </n-input>
                            <n-button ghost class=" h-auto dark:text-white " @click="addMessageListItem(route.params.uuid)">
                                发送
                            </n-button>
                        </n-input-group>

                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
    import {
        NButton, NInput, NIcon, NButtonGroup, NSpin,
        NInputGroup, NCard, NModal, NTabs, NTabPane, NInputNumber, NSelect,
        NTooltip,
        useMessage
    } from 'naive-ui'
    import { GameControllerOutline, GameController } from '@vicons/ionicons5'
    import { LogInOutline as LogInIcon, SettingsOutline, Menu } from '@vicons/ionicons5'
    import { Edit, Delete, Download ,Upload} from '@vicons/carbon'
    import Markdown from 'vue3-markdown-it';

    import { reactive, ref, getCurrentInstance, watch, watchEffect } from 'vue';
    import { useRouter, useRoute } from 'vue-router'
    import html2canvas from "html2canvas";


    const router = useRouter()
    const route = useRoute()
    const instaceV = getCurrentInstance()
    const message = useMessage()
    const fileInput = ref(null);
    const selectedImage = ref(null);
    const avatar = ref('../assets/human5.png');
    const avatarInput = ref(null);

    const handleAvatarClick = () => {
        console.log(avatar.value)
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
    // 移动端下侧边栏显影

    const showSetting = ref(false)
    var setting = reactive({
        model: 'gpt-3.5-turbo',
        Temperatures: 0.8,
        Top_p: 1,
    })

    var segmented = {
        content: 'soft',
        footer: 'soft'
    }

    var selectOptions = ref([
        {
            label: 'gpt-3.5-turbo',
            value: 'gpt-3.5-turbo'
        },
        {
            label: 'gpt-4',
            value: 'gpt-4'
        }
    ])

    var centerLodding = ref(false)

    var input_area_value = ref('')
    var left_data = reactive({
        left_list: [
            { uuid: 1, title: 'New Chat1', enable_edit: false },
            { uuid: 2, title: 'New Chat2', enable_edit: false },
        ],
        chat: [
            {
                uuid: 1, msg_list: [
                    { type: 'text',content: 'hello1', create_time: '2023-11-09 11:50:23', reversion: false, msgload: false },
                    { type: 'text',content: 'hallo', create_time: '2024-8-15 12:00:00', reversion: true, msgload: true}
                ]
            },
            {
                uuid: 2, msg_list: [
                    { type:'text', content: 'xxx', create_time: '2023-11-09 11:50:23', reversion: false, msgload: false },
                ]
            },
        ],

    })

    const handleUploadImage = () => {
        fileInput.value.click();
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
            msg_list: []
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
    function addMessageListItem(uuid) {
        var index = left_data.chat.findIndex(v => v.uuid == uuid)
        const now_t = (new Date()).toLocaleString('sv-SE', { "timeZone": "PRC" })
        if (selectedImage.value) {
            left_data.chat[index].msg_list.push({
            type: 'image',
            content: selectedImage.value,
            create_time: now_t,
            reversion: true,
            msgload: false
        });
            selectedImage.value = null;
        } else if (input_area_value.value) {
            left_data.chat[index].msg_list.push({
                type: 'text',
                content: input_area_value.value,
                create_time: now_t,
                reversion: true,
                msgload: false
        })}
        input_area_value.value = ''
        var ele = document.getElementById("msgArea")
        ele.scrollTop = ele.scrollHeight + ele.offsetHeight
        left_data.chat[index].msg_list.push({
            type: '',
            content: '',
            create_time: now_t,
            reversion: false,
            msgload: true
        })
        startStream(index)
    }

    function buildMessagePromt(index) {
        const res = []
        left_data.chat[index].msg_list.forEach(v => {
            let role = v.reversion ? 'user' : 'assistant'
            res.push({
                role: role,
                content: v.content
            })
        })
        return res
    }
    // const response = await fetch(url, {
            //     "method": "POST",
            //     "headers": {
            //         Authorization: `Bearer ${key}`
            //     },
            //     "mode": "cors",
            //     "body": JSON.stringify({
            //         model: setting.model,
            //         messages: buildMessagePromt(index),
            //         temperature: setting.Temperatures,
            //         top_p: setting.Top_p,
            //         stream: true,
            //     }),
            //     "timeout": 1000,
            // });

    async function startStream(index) {
        const url = import.meta.env.VITE_AI_BASE_URL;
        const key = import.meta.env.VITE_AI_KEY
        try {
            
            const response = await fetch(url, {
                "method": "POST",
                "headers": {
                    Authorization: `Bearer ${key}`
                },
                "mode": "cors",
                "body": JSON.stringify({
                    messages: buildMessagePromt(index),
                }),
                "timeout": 1000,
            });
            left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].msgload = false
        } catch (error) {
            left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].content += `发生了一些错误：${response.status}-${response.statusText}`
            return false
        }
    
        
        
        if (response.status !== 200) {
            left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].content += `发生了一些错误：${response.status}-${response.statusText}`
            return false
        }

        const reader = response.body.getReader();
        let buffer = ''; // 用于缓存数据块

        const readStream = async () => {

            const { done, value } = await reader.read();

            if (done) {
                console.log('Stream reading complete');
                return;
            }

            const chunk = new TextDecoder('utf-8').decode(value);
            buffer += chunk; // 将数据块追加到缓冲区中

            // 检查缓冲区中是否有完整的数据
            let completeData = '';
            let separatorIndex;
            while ((separatorIndex = buffer.indexOf('\n')) !== -1) {
                completeData = buffer.slice(0, separatorIndex); // 提取完整的数据
                buffer = buffer.slice(separatorIndex + 1); // 更新缓冲区，去掉已处理的数据

                // 解析JSON数据
                const res = completeData.split(": ")[1]
                let data;
                try {
                    data = JSON.parse(res);
                    // 这里处理业务逻辑
                    const delta_content = data.choices[0].delta.content
                    console.log(delta_content)

                    left_data.chat[index].msg_list[left_data.chat[index].msg_list.length - 1].content += delta_content
                } catch (e) {
                    // console.error('Error parsing JSON:', e);
                    continue
                }
            }

            return readStream();
        }

        // 开始处理流数据
        return readStream();
    }

    // function hasLogin(compomentName = 'Login') {
    //     console.log(instaceV.proxy.hasLogin)
    //     if (compomentName == 'Login') return instaceV.proxy.hasLogin ? 'hidden' : '';
    //     if (compomentName == 'main') return instaceV.proxy.hasLogin ? '' : 'hidden';
    // }

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
.container{
    background-image: url('/assets/算命.jpg');
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;

}
.router-link-active {
    border-color: #18a058;
    color: #18a058;
}
</style>
