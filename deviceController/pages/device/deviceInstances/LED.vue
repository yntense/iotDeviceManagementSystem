<template>
	<view class="wholePage">
	<view> 
	<view class="status-area">
		<view v-if="device.deviceState == 'offline'">
		<text style="color: red;">{{device.deviceStateCN}}</text>
		</view>
		<view v-if="device.deviceState == 'reconnect'">
		<text style="color: orange;">{{device.deviceStateCN}}</text>
		</view>
		<view v-if="device.deviceState == 'online'">
		<text style="color: green; font-weight: bold;">{{device.deviceStateCN}}</text>
		</view>
		<text style="margin-left:5px ;margin-right:5px;">:</text>
		<text>设备状态</text>
	</view>
	<view class="status-led">
		<text>LED状态</text>
		<text style="margin-left:5px ;margin-right:5px;">:</text>
		<text style="color: darkBlue; font-weight: bold;">{{device.ledStateCN}}</text>
		 
	</view>
	</view>
	<view class="content">
		<view v-if="device.ledState == 'close'">
			<image class="logo" src="/static/close.png" :data-state="ledStates.light" @click="onCtl"></image>
		</view>
		<view v-else-if="device.ledState == 'light'">
			<image class="logo" src="/static/open.png" :data-state="ledStates.close" @click="onCtl"></image>
		</view>
		<view v-else-if="device.ledState == 'blink'">
			
			<image class="blinkPic" src="/static/close.png" :data-state="ledStates.close" @click="onCtl"></image>
			<image class="blinkPic" src="/static/open.png" :data-state="ledStates.light" @click="onCtl"></image>
		</view>
		<view class="text-area">
			<button class="title" @click="onBlink">闪烁</button>
		</view>
	</view>
	<view class="pageBottom">
		<button class="closeButton" size='mini' @click="onClosePopup">关闭</button>
	</view>
	<view>
		<!-- 输入框示例 -->
		<uni-popup ref="inputDialog" type="dialog">
			<uni-popup-dialog ref="inputClose" mode="input" title="输入闪烁间隔(ms)" v-bind:value="device.blinkInterval"
				placeholder="请输入内容" @confirm="dialogInputConfirm"></uni-popup-dialog>
		</uni-popup>
	</view>
	</view>
</template>

<script>
var mqtt = require('module/mqtt/dist/mqtt.js')
const mqttOptions = {
	keepalive: 30,
	clean: false, 
	connectTimeout: 5000, // Timeout
	clientId: 12345,
	username: 'test',
	password: 'public',
}
var LED_STATE_MAP = new Map()
LED_STATE_MAP.set('light','已点亮')
LED_STATE_MAP.set('close','已关闭')
LED_STATE_MAP.set('blink','闪烁中')
const LED_STATE = ['light','close','blink']
var LOCAL_DEVICE_ID = "mini-code"
var CONTROL_TOPIC = ''
var STATE_TOPIC = ''
var CONTROL_RECEIVE_TOPIC = ''
var mqttClient 
	export default {
		props:{
			deviceInstance:{
				type: Object,
			}
		},
		data() {
			return {
				title: 'Hello',
				device:{
					deviceState: 'offline',
					deviceStateCN:'已离线',
					ledState: "close",
					ledStateCN: "已关闭",
					blinkInterval: '1000',
				},
				ledStates:
				{
					light: 'light',
					close: 'close',
					blink: 'blink'
				}
			}
		},
		computed: {
			//监听数据变化，对象中的具体值
		　　deviceState() {
		　　　　return this.device.deviceState
		　　},
			ledState() {
		　　　　return this.device.ledState
		　　},
			blinkInterval() {
		　　　　return this.device.blinkInterval
		　　}
		},
		watch:{
			//监听数据变化，对象中的具体值
			deviceState(newVal,oldVal){
				if(newVal == 'offline')
				{
					this.device.deviceStateCN = '已离线'
				}else if(newVal == 'online')
				{
					this.device.deviceStateCN = '在线'
				}else if(newVal == 'reconnect')
				{
					this.device.deviceStateCN = '正在重连'
				}
			},
			ledState(newVal,oldVal) {
				if(newVal != 'blink')
				{
					this.device.ledStateCN = LED_STATE_MAP.get(newVal)
				}else{
					this.device.ledStateCN = LED_STATE_MAP.get(newVal) + ':' + this.device.blinkInterval + 'ms'
				}
				
			},
			blinkInterval(newVal,oldVal) {
				if(this.device.ledState == 'blink')
				{
					this.device.ledStateCN = LED_STATE_MAP.get('blink') + ':' + newVal + 'ms'
					
				}
			}
		},
		methods: {
			onCtl(e){
				let state = e.currentTarget.dataset.state
				console.log(state)
				if(state == "close"){
					let msg = {
						msgId: 100,
						clientID: LOCAL_DEVICE_ID,
						operation: 0,
						destSubDevice: "led",
						arg:1,
						payload: this.device.blinkInterval
					}
					let msgJson = JSON.stringify(msg)
					mqttClient.publish(CONTROL_TOPIC, msgJson)
				}else if(state == "light"){
					let msg = {
						msgId: 100,
						clientID: LOCAL_DEVICE_ID,
						operation: 0,
						destSubDevice: "led",
						arg:0,
						payload: this.device.blinkInterval
					}
					let msgJson = JSON.stringify(msg)
					mqttClient.publish(CONTROL_TOPIC, msgJson)	
				}
			},
			onBlink(){
				if(this.isDeviceOnline())
				{
					this.$refs.inputDialog.open()
				}else{
					uni.showLoading({
						title: '找不到设备！'
					})
					setTimeout(() => {
						uni.hideLoading()
					}, 500)
				}
				
			},
			dialogInputConfirm(val){
				uni.showLoading({
					title: ''
				})
				console.log(val)
				this.device.blinkInterval = parseInt(val)
				let msg = {
					msgId: 100,
					clientID: LOCAL_DEVICE_ID,
					operation: 0,
					destSubDevice: "led",
					arg:2,
					payload: this.device.blinkInterval
				}
				let msgJson = JSON.stringify(msg)
				mqttClient.publish(CONTROL_TOPIC, msgJson)	
				setTimeout(() => {
					uni.hideLoading()
					// 关闭窗口后，恢复默认内容
					this.$refs.inputDialog.close()
				}, 1000)
			},
			isDeviceOnline(){
				if(this.device.deviceState == "online")
				{
					return true
				}
				return false
			},
			onClosePopup(e){
				console.log(e)
				//通知父组件
				this.$emit('fatherMethod', "closePopup")
				
			}

		},
		mounted(){
			CONTROL_RECEIVE_TOPIC = '/' + LOCAL_DEVICE_ID + '/control/response'  
			CONTROL_TOPIC = '/' + this.deviceInstance.deviceID + '/' + "control"
			STATE_TOPIC = '/' + this.deviceInstance.deviceID + '/' + "state"
			const mqttOptions = {
			    keepalive: 30,
			    clean: false, 
			    connectTimeout: 5000, // Timeout
			    clientId: 12345,
			    username: 'test',
			    password: 'public',
			}
			mqttClient = mqtt.connect('ws://www.beatingcai.com:8083/mqtt', mqttOptions)
			mqttClient.on('connect', () => {
			 //    this.device.deviceState = 'online'
				mqttClient.subscribe(CONTROL_RECEIVE_TOPIC, (err) => {
				       console.log(err)
				    })
					mqttClient.subscribe(STATE_TOPIC, (err) => {
					       console.log(err)
					    })
			});
			// 自动重连
			mqttClient.on('reconnect', (msg) => {
				this.device.deviceState = 'reconnect'
			});
			// 错误
			mqttClient.on('error', () => {
			    console.log('error')
			});
			// 断开
			mqttClient.on('end', () => {
			    console.log('end')
			});
			// 掉线
			mqttClient.on('offline', (msg) => {
				this.device.deviceState = 'offline'
			});
			// 收到消息        
			mqttClient.on('message', (topic, message) => {
			    // 把arrayBuffer转成字符串
				if(CONTROL_RECEIVE_TOPIC == topic)
				{
					var json = JSON.parse(new String(message, "UTF-8"))
					console.log(json)
				}else if(STATE_TOPIC == topic)
				{
					if(new String(message, "UTF-8") == 'offline')
					{
						this.device.deviceState = 'offline'
						return
					}
					try{
						var json = JSON.parse(new String(message, "UTF-8"));
						this.device.ledState = LED_STATE[json.State]
						this.device.blinkInterval = json.interval
						this.device.deviceState = 'online'
						console.log(topic,json)
					}catch(e){
					
						//TODO handle the exception
					}	
				}
			})
				
		},
		beforeDestroy(){
			mqttClient.end()
		}
	}
</script>

<style>
	.wholePage{
		width: 80vw;
		height: 80vh;
	}
	.content {
		width: 100%;
		height: 60vh;
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
	.blinkPic{
		height: 200rpx;
		width: 200rpx;
		margin-top: 200rpx;
		margin-left: 50rpx;
		margin-right: 50rpx;
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
	
	.status-area{
		display: flex;
		flex-direction: row-reverse;
		align-items: center;
		margin-top: 10px;
		margin-right: 20px;
	}
	.status-led{
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: center;
		margin-top: 10px;
	}
	
	.pageBottom{
		/* height: 20vh; */
		margin-top: 10px;
		display: flex;
		flex-direction: row;
	}
	.closeButton{
		margin-right: 100px;
	}
</style>
