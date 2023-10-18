<template>
    <h1>{{msg}}</h1>
</template>

<script>
export default {
  name: 'DescriptionComponent',
    data() {
        return {
            msg: ''
        }
    },
    mounted(){
        fetch("/describe", {
            method: "POST",
             body: JSON.stringify({
             "image": "dGVzdA==",
             "language": "EN"
             }),
             headers: {
                "Content-type": "application/json"
             }
        })
            .then((response) => response.text())
            .then((data) => {
            this.msg = data;
            })
    }
}
</script>

