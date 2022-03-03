<script>
// import { get } from '@vueuse/core'
import axios from 'axios'
// import { throwError } from 'element-plus/lib/utils'
export default {
    name: 'ConsoleDesk',
    props: {},
    data() {
        return {
            bot_start_return: false,
            bot_stop_return: false,
            zion_start_return: false,
            zion_stop_return: false,
            botlog: '',
            zionlog: ''
        }
    },
    created() {
        setInterval(this.readBotlog, 1000)
        setInterval(this.readZionlog, 1000)
    },
    mounted() {
    },
    methods: {
        async bot_start() {
            this.bot_start_return = true
            const {
                data: bot_start_return
            } = await axios.get('http://localhost:8044/bot/start')
            console.log(bot_start_return)
            this.bot_start_return = bot_start_return.status
        },
        async bot_stop() {
            this.bot_stop_return = true
            const {
                data: bot_stop_return
            } = await axios.get('http://localhost:8044/bot/stop')
            console.log(bot_stop_return)
            this.bot_stop_return = bot_stop_return.status
        },
        async zion_start() {
            this.zion_start_return = true
            const {
                data: zion_start_return
            } = await axios.get('http://localhost:8044/zion/start')
            console.log(zion_start_return)
            this.zion_start_return = zion_start_return.status
        },
        async zion_stop() {
            this.zion_stop_return = true
            const {
                data: zion_stop_return
            } = await axios.get('http://localhost:8044/zion/stop')
            console.log(zion_stop_return)
            this.zion_stop_return = zion_stop_return.status
        },
        readBotlog() {
            const file = this.loadFile('JiangHs/bot.log')
            // console.info(file)
            // console.log(this.unicodeToUtf8(file))
            this.botlog = this.unicodeToUtf8(file)
            // return this.unicodeToUtf8(file)
        },
        readZionlog() {
            const file = this.loadFile('JiangHs/zion.log')
            // console.info(file)
            // console.log(this.unicodeToUtf8(file))
            this.zionlog = this.unicodeToUtf8(file)
            // return this.unicodeToUtf8(file)
        },
        // 读取文件
        loadFile(name) {
            const xhr = new XMLHttpRequest()
            const okStatus = document.location.protocol === 'file:' ? 0 : 200
            xhr.open('GET', name, false)
            xhr.overrideMimeType('text/html;charset=utf-8')// 默认为utf-8
            xhr.send(null)
            return xhr.status === okStatus ? xhr.responseText : null
        },
        // unicode转utf-8
        unicodeToUtf8(data) {
            data = data.replace(/\\/g, '%')
            return unescape(data)
        }

    }
}
</script>

<template>
    <div>
        <page-header title="主要控制台" content="JianHs" />
        <el-row :gutter="20" style="margin: -10px 10px;">
            <el-col :md="12">
                <page-main style="margin: 10px 0;">
                    机器人：
                    <el-button type="primary" :loading="bot_start_return" @click="bot_start()">启动</el-button>
                    <el-button type="danger" :loading="bot_stop_return" @click="bot_stop()">停止</el-button>
                </page-main>
            </el-col>
            <el-col :md="12">
                <page-main style="margin: 10px 0;">
                    主账户：
                    <el-button type="primary" :loading="zion_start_return" @click="zion_start()">启动</el-button>
                    <el-button type="danger" :loading="zion_stop_return" @click="zion_stop()">停止</el-button>
                </page-main>
            </el-col>
        </el-row>
        <el-row :gutter="20" style="margin: -10px 10px;">
            <el-col :md="12">
                <page-main style="margin: 10px 0;height: 400px">
                    机器人日志：
                    <page-main style="margin: 10px 0;height: 335px;background:black;color:green;font-size:10px">
                        <pre>{{ botlog }}</pre>
                    </page-main>
                </page-main>
            </el-col>
            <el-col :md="12">
                <page-main style="margin: 10px 0;height: 400px">
                    主账户日志：
                    <page-main style="margin: 10px 0;height: 335px;background:black;color:green;font-size:10px">
                        <pre>{{ zionlog }}</pre>
                    </page-main>
                </page-main>
            </el-col>
        </el-row>
        <page-main>
            PageMain 是最常用的页面组件，几乎所有页面都会使用到
        </page-main>
        <page-main title="你可以设置一个自定义的标题">
            这里放页面内容
        </page-main>
        <page-main title="带展开功能" collaspe height="200px">
            <h1>Fantastic-admin</h1>
            <img src="../../assets/images/logo.png">
            <p>这是一款开箱即用的中后台框架，同时它也经历过数十个真实项目的技术沉淀，确保框架在开发中可落地、可使用、可维护</p>
        </page-main>
    </div>
</template>
