<script>
import axios from 'axios'
// import { throwError } from 'element-plus/lib/utils'
export default {
    name: 'StatisticsBatchactionbar',
    props: {},
    data() {
        return {
            video: [],
            // file_id: 'BAACAgUAAx0CZ8v_7QACc11h_fNSs14XXt6dueUE5Dd126XpRwAC0wAE28hWWQ-oVY1EI8MeBA',
            // file_unique_id: 'AgAD0wAE28hW',
            // file_name: null,
            // width: '360',
            // height: '640',
            // duration: '124',
            // mime_type: 'video/mp4',
            // file_size: '6882411',
            // supports_streaming: '1',
            // thumbs_file_id: 'AAMCBQADHQJny__tAAJzXWH981KzXhde3p255QTkN3XbpelHAALTAATbyFZZD6hVjUQjwwAIAQAHbQAHHgQ',
            // thumbs_width: '180',
            // thumbs_height: '320',
            // thumbs_file_size: '11036',
            // type: 'video',
            // from_user_id: '5076551961',
            // message_id: '29533'
            selectionDataList: [],
            totle: 100
        }
    },
    created() {
        this.editBtn(1),
        this.get_count()
    },
    mounted() {},
    methods: {
        async editBtn(limit) {
            const {
                data: res
            } = await axios.get(`http://23.225.15.47:3000/api/user/video/${limit}`)
            // console.log(res)
            this.video = res
        },
        async get_count() {
            const {
                data: res
            } = await axios.get('http://23.225.15.47:3000/api/user/videocount')
            this.totle = res[0].count
            // document.getElementById('count').innerHTML = '总数：' + res[0].count
            // console.log(this.aboutpage.totle)
        },
        handleCurrentChange(val) {
            // console.log(`当前页: ${val}`)
            this.editBtn(val)
        }
    }

}
</script>

<template>
    <div>
        <page-header title="视频数据">
            <template #content>
                <!-- <p>BatchActionBar</p>
                <p style="margin-bottom: 0;">该组件需要和 ElTable 搭配使用</p> -->
            </template>
        </page-header>
        <page-main>
            <!-- <batch-action-bar :data="dataList" :selection-data="selectionDataList" @check-all="$refs.table.toggleAllSelection()" @check-null="$refs.table.clearSelection()">
                <el-button size="default">单个批量操作按钮</el-button>
                <el-button-group>
                    <el-button size="default">批量操作按钮组1</el-button>
                    <el-button size="default">批量操作按钮组2</el-button>
                </el-button-group>
            </batch-action-bar> -->
            <el-table ref="table" :data="video" border stripe highlight-current-row @selection-change="selectionDataList = $event">
                <el-table-column type="selection" width="40" />
                <el-table-column prop="file_id" label="file_id" width="180" />
                <el-table-column prop="file_unique_id" label="file_unique_id" width="140" />
                <el-table-column pro="file_name" label="file_name" />
                <el-table-column prop="width" label="width" width="70" />
                <el-table-column prop="height" label="height" width="70" />
                <el-table-column prop="duration" label="duration" width="70" />
                <el-table-column prop="mime_type" label="mime_type" />
                <el-table-column prop="file_size" label="file_size" />
                <el-table-column prop="supports_streaming" label="supports_streaming" />
                <el-table-column prop="thumbs_file_id" label="thumbs_file_id" width="180" />
                <el-table-column prop="thumbs_width" label="thumbs_width" width="70" />
                <el-table-column prop="thumbs_height" label="thumbs_height" width="70" />
                <el-table-column prop="thumbs_file_size" label="thumbs_file_size" />
                <el-table-column prop="type" label="type" />
                <el-table-column prop="from_user_id" label="from_user_id" />
                <el-table-column prop="message_id" label="message_id" />
            </el-table>
            <batch-action-bar :data="video" :selection-data="selectionDataList" @check-all="$refs.table.toggleAllSelection()" @check-null="$refs.table.clearSelection()">
                <el-button size="default @click='delet">删除</el-button>
                <!-- <el-button size="default" @click="editBtn">刷新</el-button> -->
                <!-- <el-button-group>
                    <el-button size="default">批量操作按钮组1</el-button>
                    <el-button size="default">批量操作按钮组2</el-button>
                </el-button-group> -->
            </batch-action-bar>
            <!-- <p id="count" /> -->
            <div id="block">
                <el-pagination
                    layout="prev, pager, next, total, jumper"
                    :page-size="10"
                    :total="parseInt(totle)"
                    @current-change="handleCurrentChange"
                />
            </div>
        </page-main>
    </div>
</template>
