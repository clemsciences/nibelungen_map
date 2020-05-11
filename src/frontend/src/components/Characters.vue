<template>
    <d3-network ref="net" :net-nodes="nodes" :net-links="links" :options="options" :link-cb="lcb"/>
</template>

<script>
    import D3Network from 'vue-d3-network'
    export default {
        name: "Characters",

        components: {
            D3Network
        },
        data: function () {
            return {
                force: 100,
                width: 500,
                height: 300,

                nodes: [
                    {id: "Siegfried", group: 1, name: "Siegfried"},
                    {id: "Brünhild", group: 1, name: "Brünhild"},
                    {id: "Gunther", group: 1, name: "Gunther"},
                    {id: "Kriemhield", group: 1, name: "Kriemhild"},
                ],
                links: [
                    {sid: "Siegfried", tid: "Brünhild", name: "Amant", _color: "#323232"}
                ],
                canvas: true,
                nodeSize: 10,
            }
        },
        computed: {
            options() {
                return {
                    // force: 3000,
                    size: {
                        w: this.w,
                        h: this.h
                    },
                    nodeSize: this.nodeSize,
                    linkWidth: 2,
                    nodeLabels: true,
                    linkLabels: true,
                    canvas: this.canvas,


                }
            },
        },
        methods: {
            lcb (link) {
              return link
            }
        }


    }
</script>

<style scoped>

.node-label{
  font-size: .5em;
}
.link-label{
  fill: purple;
  transform: translate(0,.5em);
  font-size: .8em;
}
.net-svg >>> .link {
    fill: bisque;
}
.net-svg >>> .node {
    fill: darkred;
}
</style>