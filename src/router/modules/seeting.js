const Layout = () => import('@/layout/index.vue')

export default {
    path: '/seeting',
    component: Layout,
    redirect: '/seeting/actionbar',
    name: 'seeting',
    meta: {
        title: '设置',
        icon: 'sidebar-menu'
    },
    children: [
        {
            path: 'baseseeting',
            name: 'seeting.baseseeting',
            component: () => import('@/views/component_extend_example/seeting.pagemain.vue'),
            meta: {
                title: '基本配置'
            }
        }
    ]
}
