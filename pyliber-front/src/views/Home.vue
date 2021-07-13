<template>
    <div class="home">
        <div v-for="i in Object.entries(pipList)" :key="i[0]">
            <router-link :to="{path:'/ModuleDetail',query:{moduleName:i[0]}}">{{i[0]}}=>{{i[1]}}</router-link>
        </div>
    </div>
</template>

<script>
    const api = require("../api.ts");
    export default ({
        data() {
            return {
                pipList: {},
            }
        },
        mounted() {
            api.pipList().then(resp => {
                this.pipList = resp.data;
            })
        }
    });
</script>
