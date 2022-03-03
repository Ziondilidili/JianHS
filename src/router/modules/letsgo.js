const Layout = () => import('@/layout/index.vue')

export default {
    path: '/letsgo',
    component: Layout,
    redirect: '/etsgo/actionbar',
    name: 'letsgo',
    meta: {
        title: 'letsgo',
        icon: 'el-icon-promotion'
    },
    children: [
        {
            path: 'actionbar',
            name: 'test.actionbar',
            component: () => import('@/views/component_extend_example/letsgo.pargemain.vue'),
            meta: {
                title: '运行'
            }
        }
    ]
}
