<template>
	<view class="content">
		<image class="logo" src="/static/logo.png"></image>
		<view class="text-area">
			<text class="title">{{title}}</text>
		</view>
	</view>
</template>

<script>	
var mqtt = require('module/mqtt/dist/mqtt.js')
	export default {
		data() {
			return {

			}
		},
		onLoad: function() {
			const mqttOptions = {
			    keepalive: 30,
			    clean: false, 
			    connectTimeout: 5000, // Timeout
			    clientId: 12345,
			    username: 'test',
			    password: 'public',
			}
			var client = mqtt.connect('wss://www.beatingcai.com:8085/mqtt', mqttOptions)
			client.on('connect', () => {
			    console.log('connect')
				client.subscribe('/BFEBFBFF000806EC/control', (err) => {
				       console.log(err)
				    })
					client.subscribe('/BFEBFBFF000806EC/state', (err) => {
					       console.log(err)
					    })
			});
			// 自动重连
			client.on('reconnect', (msg) => {
			    console.log('reconnect', msg)
			});
			// 错误
			client.on('error', () => {
			    console.log('error')
			});
			// 断开
			client.on('end', () => {
			    console.log('end')
			});
			// 掉线
			client.on('offline', (msg) => {
			    console.log('offline',msg)
			});
			// 收到消息        
			client.on('message', (topic, message) => {
			    // 把arrayBuffer转成字符串
				// var json = JSON.parse(new String(message, "UTF-8"));
				// console.log(topic,json)
			})
			// var socketTask = uni.connectSocket({
			// 	url: 'wss://www.beatingcai.com:8085/mqtt', 
			// 	complete: (res)=> {
			// 		console.log(res)
			// 		},
			// 		fail: (res)=> {
			// 			console.log(res)
			// 			}
			// })
		},
		methods: {

		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 200rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>
