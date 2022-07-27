<template>
	<view>
		<view style="padding-top: 5px;"></view>
		<uni-section title="查找设备" type="line">
			<view class="top-container">
				<uni-search-bar @confirm="onSearchDevice" :focus="true" v-model="searchValue"
					 @clear="clear" placeholder="请输入设备ID" clearButton="auto" cancelButton="none">
				</uni-search-bar>	
				<button class="uni-button addDeviceStyle" size="mini" type="primary" @click="onAddDevice('info')">添加设备</button>
			</view>
		</uni-section>

		<view class="uni-container" style="padding-top: 15px;">
			<uni-table ref="table" :loading="loading" border stripe type="selection" emptyText="暂无更多数据" @selection-change="selectionChange">
				<uni-tr class="tableTitle">
					<uni-th width="150" align="center">设备名</uni-th>
					<uni-th width="150" align="center">设备类型</uni-th>
					<uni-th align="center">设备ID</uni-th>
					<uni-th align="center">设备状态</uni-th>
					<uni-th width="204" align="center">设置</uni-th>
				</uni-tr>
				<uni-tr v-for="(item, index) in tableData" :key="index">
					<uni-td>{{ item.deviceName }}</uni-td>
					<uni-td align="center">
						<view class="name">{{ item.deviceType }}</view>
					</uni-td>
					<uni-td align="center">{{ item.deviceID }}</uni-td>
					<uni-td align="center">{{ item.deviceState }}</uni-td>
					<uni-td>
						<view class="uni-group">
							<button class="uni-button" size="mini" type="primary" :data-device='item' @click="ctl" >控制</button>
							<button class="uni-button" size="mini" type="warn" :data-device='item' @click="onDeleteDevice(item.deviceID)">删除</button>
						</view>
					</uni-td>
				</uni-tr>
			</uni-table>
			<view class="uni-pagination-box"><uni-pagination show-icon :page-size="pageSize" :current="pageCurrent" :total="total" @change="change" /></view>
		
		</view>
		<view style="position:absolute; bottom: 5vh;left:40%;">
			<uni-link href="https://beian.miit.gov.cn/" text="闽ICP备2021002444号-1"></uni-link>
		</view>
				

		<view>
			<!-- 普通弹窗 -->
			<uni-popup ref="popup" background-color="#fff" :is-mask-click="false">
				<view class="popup-content" :class="{ 'popup-height': type === 'left' || type === 'right' }">
					<LED class="text" v-bind:deviceInstance="device" @fatherMethod="onLedMessage"></LED>
			    </view>
			</uni-popup>
		</view>
		<view>
			<!-- 提示窗示例 -->
			<uni-popup ref="alertDialog" type="dialog">
				<uni-popup-dialog :type="msgType" title="添加设备" @confirm="dialogConfirm"
					@close="dialogClose">
					<view class="addDeviceContainer" style="width: 100%;" >
					<button style="width: 100%;margin-bottom: 5px;" type="primary" plain="true" @click="onAddDeviceform('scan')">扫一扫</button>
					<button style="width: 100%;" type="default" plain="true" @click="onAddDeviceform('hand')">手动添加</button>
					</view>
					</uni-popup-dialog>
			</uni-popup>
		</view>
		<!-- 添加设备窗示例 -->
			<uni-popup ref="addDeviceDialog" type="dialog">
				<uni-popup-dialog :type="msgType" title="输入设备信息" @confirm="submit('valiForm')"
					@close="onAddDeviceDialogClose" beforeClose=true>
		<uni-section >
			<view class="example">
				<!-- 基础表单校验 -->
				<uni-forms ref="valiForm" :rules="rules" :modelValue="valiFormData">
					<uni-forms-item label="设备名" required name="deviceName">
						<uni-easyinput v-model="valiFormData.deviceName" placeholder="请输入设备名" />
					</uni-forms-item>
					<uni-forms-item label="设备ID" required name="deviceID">
						<uni-easyinput v-model="valiFormData.deviceID" placeholder="请输入设备ID" />
					</uni-forms-item>
					<uni-forms-item label="设备类型" required name="deviceType">
						<uni-easyinput v-model="valiFormData.deviceType" placeholder="请输入设备类型" />
					</uni-forms-item>
				</uni-forms>
			</view>
		</uni-section>
					</uni-popup-dialog>
			</uni-popup>
		</view>
</template>

<script>
// import tableData from './tableData.js'
 import LED from './deviceInstances/LED'
 import {url} from '@/config/config'

export default {
	components:{
		LED
	},
	data() {
		return {
			searchVal: '',
			tableData: [],
			// 每页数据量
			pageSize: 10,
			// 当前页
			pageCurrent: 1,
			// 数据总量
			total: 0,
			loading: false,
			// 弹窗
			type: 'center',
			//传递设备参数
			device: null,
			
			msgType:'success',
			
			// 校验表单数据
			valiFormData: {
				deviceID: '',
				deviceName: '',
				deviceType: '',
			},
			// 校验规则
			rules: {
				deviceID: {
					rules: [{
						required: true,
						errorMessage: '设备ID不能为空'
					}]
				},
				deviceName: {
					rules: [{
						required: true,
						errorMessage: '设备名不能为空'
					}]
				},
				deviceType: {
					rules: [{
						required: true,
						errorMessage: '设备类型不能为空'
					}]
				}
			},
			//搜索设备
			searchValue:''
		}
	},
	onLoad() {
		console.log('relaod')
		//获取总设备数
		//登陆操作
		let that = this
		this.selectedIndexs = []
		this.getData(1)
	},
	methods: {
		// 多选处理
		selectedItems() {
			return this.selectedIndexs.map(i => this.tableData[i])
		},
		// 多选
		selectionChange(e) {
			console.log(e.detail.index)
			this.selectedIndexs = e.detail.index
		},
		//批量删除
		delTable() {
			console.log(this.selectedItems())
		},
		// 分页触发
		change(e) {
			this.$refs.table.clearSelection()
			this.selectedIndexs.length = 0
			this.getData(e.current)
		},
		// 搜索
		search() {
			this.getData(1, this.searchVal)
		},
		// 获取数据
		getData(pageCurrent, value = '') {
			this.loading = true
			this.pageCurrent = pageCurrent
			this.request({
				pageSize: this.pageSize,
				pageCurrent: pageCurrent,
				value: value,
				success: res => {
					// console.log('data', res);
					this.tableData = res.data
					this.total = res.total
					this.loading = false
				}
			})
		},
		// 伪request请求
		request(options) {
			const { pageSize, pageCurrent, success, value } = options
			let that = this
			uni.request({
				url: url.DeviceURL + 'getDevices/',
				header:{
					authorization :uni.getStorageSync("session")
				},
				method:'POST',
				data:{
					"startIndex": (pageCurrent-1)*pageSize,
					"count":pageSize
				},
				dataType:'json',
				success(res) {
					if(res.data.error == 0)
					{
						var devices = res.data.iotDevice
						if(devices.length == 0)
						{
							if(pageCurrent == 1){
								typeof success === 'function' &&
									success({
										data: devices,
										total: res.data.totalCount 
									})
								return
							}
							that.getData(pageCurrent-1)
							return
						}
						console.log(devices)
						typeof success === 'function' &&
							success({
								data: devices,
								total: res.data.totalCount 
							})
					}
				},fail(res) {
					console.log(res)
				}
			})
			// let total = tableData.length
			// let data = tableData.filter((item, index) => {
			// 	const idx = index - (pageCurrent - 1) * pageSize
			// 	return idx < pageSize && idx >= 0
			// })
			// console.log(data)
			// if (value) {
			// 	data = []
			// 	tableData.forEach(item => {
			// 		if (item.name.indexOf(value) !== -1) {
			// 			data.push(item)
			// 		}
			// 	})
			// 	total = data.length
			// }

			// setTimeout(() => {
			// 	typeof success === 'function' &&
			// 		success({
			// 			data: data,
			// 			total: total
			// 		})
			// }, 500)
		},
		ctl(e)
		{
			let device = e.currentTarget.dataset.device
			this.device = device
			this.$refs.popup.open('center')
			
		},
		onLedMessage(message)
		{
			if(message == 'closePopup')
			{
				this.$refs.popup.close()
			}
		},
		onAddDevice(type){
			this.msgType = type
			this.$refs.alertDialog.open('center')
		},
		onAddDeviceform(form)
		{
			if(form == 'scan')
			{
				//起调摄像头
			}else if(form == 'hand')
			{
				this.$refs.alertDialog.close()
				this.$refs.addDeviceDialog.open('center')
			}
		},
		submit(ref) {
			let that = this
			this.$refs[ref].validate().then(res => {
			uni.request({
				url: url.DeviceURL + 'add/',
				header:{
					authorization :uni.getStorageSync("session")
				},
				method:'POST',
				data:{
					"device_id": that.valiFormData.deviceID,
					"device_name": that.valiFormData.deviceName,
					"device_type": that.valiFormData.deviceType
				},
				dataType:'json',
				success(res) {
					if(res.data.error == 0)
					{
						that.getData(that.pageCurrent)
						uni.showToast({
							title:res.data.msg
						})
					}else if(res.data.error == -1)
					{
						uni.showToast({
							title:res.data.msg
						})	
					}
				},fail(res) {
					console.log(res)
				}
			})
				this.$refs.addDeviceDialog.close()
			}).catch(err => {
				console.log('err', err);
			})
		},
		onAddDeviceDialogClose()
		{
			this.$refs.addDeviceDialog.close()
		},
		onDeleteDevice(deviceID)
		{
			let that = this
			uni.request({
				url: url.DeviceURL + 'delete/',
				header:{
					authorization :uni.getStorageSync("session")
				},
				method:'POST',
				data:{
					"device_id": deviceID,
				},
				dataType:'json',
				success(res) {
					if(res.data.error == 0)
					{
						//更新当前页
						that.getData(that.pageCurrent)
						uni.showToast({
							title:res.data.msg
						})
						
					}else if(res.data.error == -1)
					{
						uni.showToast({
							title:res.data.msg
						})	
					}
				},fail(res) {
					console.log(res)
				}
			})
		},
		onSearchDevice()
		{
			let that = this
			uni.request({
				url: url.DeviceURL + 'find/',
				header:{
					authorization :uni.getStorageSync("session")
				},
				method:'POST',
				data:{
					"device_id": that.searchValue,
				},
				dataType:'json',
				success(res) {
					if(res.data.error == 0)
					{
						//更新当前页
						that.loading = true
						let device = res.data.device
						that.tableData = device
						that.total = device.length
						that.loading = false
						
					}else if(res.data.error == -1)
					{
						uni.showToast({
							title:res.data.msg
						})	
					}
				},fail(res) {
					console.log(res)
				}
			})
		},
		//清除搜索框
		clear() {
			this.getData(this.pageCurrent)
		}
	}
}
</script>

<style>
/* #ifndef H5 */
/* page {
	padding-top: 85px;
} */
/* #endif */

.top-container{
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-between;
}

.addDeviceContainer{
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;	
}
 .addDeviceStyle{
	margin-right: 10px; 
 }
 
.tableTitle{
/* 	background-color: lightgray;
	color: #000000!important; */
}
.uni-container{
	padding-top:5px;
}
.uni-group {
	display: flex;
	align-items: center;
}
</style>
